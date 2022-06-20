# manipulate some of the dataframes in Pandas, to speed up the process

import pandas as pd

# movies of interest, list comes from R file
MOVIE_IDS = ["tt0050083", "tt0062622", "tt0066921", "tt0026778", "tt0044081",
             "tt0042192", "tt0074119", "tt0069704", "tt0075686", "tt0078788",
             "tt0052618", "tt0083658", "tt0061418", "tt0029947", "tt0064115",
             "tt0068327", "tt0034583", "tt0071315", "tt0033467", "tt0021749",
             "tt0097216", "tt0036775", "tt0057012", "tt0023969", "tt0064276", 
             "tt0109830", "tt0031381", "tt0099685", "tt0044706", "tt0061811",
             "tt0025316", "tt0038650", "tt0073195", "tt0024216", "tt0056172",
             "tt0066026", "tt0064665", "tt0027977", "tt0031679", "tt0073440",
             "tt0074958", "tt0053125", "tt0047296", "tt0073486", "tt0091763",
             "tt0054215", "tt0110912", "tt0081398", "tt0082971", "tt0047396",
             "tt0075148", "tt0120815", "tt0108052", "tt0046303", "tt0045152",
             "tt0029583", "tt0053291", "tt0084707", "tt0054331", "tt0076759",
             "tt0034240", "tt0018455", "tt0043014", "tt0028333", "tt0075314",
             "tt0043265", "tt0053604", "tt0036868", "tt0050212", "tt0077416", 
             "tt0067116", "tt0017925", "tt0068646", "tt0071562", "tt0015864",
             "tt0061722", "tt0032551", "tt0067328", "tt0120737", "tt0033870",
             "tt0032904", "tt0049730", "tt0111161", "tt0102926", "tt0167404",
             "tt0059742", "tt0040897", "tt0065214", "tt0032138", "tt0120338",
             "tt0056592", "tt0084805", "tt0114709", "tt0105695", "tt0052357",
             "tt0055614", "tt0061184", "tt0035575"]

class CrewReader:
    """
    Class to read and process information about the crew

    :param crew_file: filepath to the file which contains crew information
    :param actors_file: filepath to the actors
    :param names_file: filepath to mapping between IDs and names
    :param crew: Pandas df, with crew information
    :param actors: Pandas df, with actors information
    :param names: Pandas df, with names information
    :param merged_crew: Pandas df, combines directors, actors and writers for a given movie
    """
    crew_file: str
    principals_file: str
    names_file: str
    crew: pd.DataFrame
    principals: pd.DataFrame
    names: pd.DataFrame
    merged_crew: pd.DataFrame

    def __init__(self, crew_file: str, principals_file: str, names_file: str):
        """
        Initializes the class by reading in the files into the appropriate dataframes. 
        """

        # read in files
        self.crew = pd.read_csv(crew_file, delimiter="\t")
        self.principals = pd.read_csv(principals_file, delimiter="\t")
        self.names = pd.read_csv(names_file, delimiter="\t")

        # filter to only keep the movies of interest
        self.crew = self.crew.loc[self.crew.tconst.isin(MOVIE_IDS)]
        self.principals = self.principals.loc[self.principals.tconst.isin(MOVIE_IDS)]

    def merge_crew(self):
        """
        Create a new dataset, which combines crew and actor together. Splits the values in each column on commas
        """
        # filter principals for actors only
        actors = self.principals.loc[self.principals.category == "actor",]

        # aggregate actors
        actors = actors.groupby("tconst")["nconst"].apply(lambda x: ','.join(x)).reset_index()

        print(actors)

        # merge actors and writers/directors into a single dataset
        self.merged_crew = pd.merge(left=self.crew, right=actors, how="inner")

        print(self.merged_crew.shape)
        
        # split fields in columns along commas
        self.merged_crew.directors = self.merged_crew.directors.str.split(',')
        self.merged_crew.writers = self.merged_crew.writers.str.split(',')
        self.merged_crew["actors"]= self.merged_crew.nconst.str.split(',')

        # only keep columns with the nconst we want to map
        self.merged_crew = self.merged_crew[['tconst', 'directors', 'writers', 'actors']]

        print(self.merged_crew.shape)
        print(self.merged_crew)


    def map_crew(self):
        """
        Uses the names df to map nconst to actual names
        """
        # store the mapping, to avoid re-searching
        mappings = {}

        # iterate through all the rows
        for i in range(len(self.merged_crew)):
            # iterate through the columns: 2nd, 3rd and last columns are the columns of interest
            for j in [1,2,3]:
                # get the field value
                field = self.merged_crew.iloc[i,j]

                # list of names to return
                names = []

                for nconst in field:
                    # try and query the mapping (speed up the search)
                    if nconst in mappings:
                        name = mappings[nconst]
                    else:
                        # get the mapping and store
                        name = self.names.loc[self.names.nconst == nconst, "primaryName"].values[0]
                        mappings[nconst] = name

                    print(name)

                    names.append(name)

                # replace
                self.merged_crew.iloc[i,j] = names

    def write_to_csv(self, output_file: str):
        """
        Write the modified dataset, with directors, actors and writers, to CSV
        """
        self.merged_crew.to_csv(output_file)



if __name__ == "__main__":
    # initialize the class with the files
    crew_reader = CrewReader("title.crew.tsv.gz", "title.principals.tsv.gz", "name.basics.tsv.gz")

    # merge the crew information
    crew_reader.merge_crew()

    # get the name instead of the tconst
    crew_reader.map_crew()

    # write the file to csv
    crew_reader.write_to_csv("crew_info.csv")