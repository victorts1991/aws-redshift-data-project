class RedshiftDdlDmlQueries:
    
    def __init__(self, redshift_client, aws_iam_role):
        self.redshift_client = redshift_client
        self.aws_iam_role = aws_iam_role

    def create_flights_table_copy_csv(self):
        self.redshift_client.execute_query(
            f"""
            CREATE TABLE flights (
                year           smallint,
                month          smallint,
                day            smallint,
                carrier        varchar(80) DISTKEY,
                origin         char(3),
                dest           char(3),
                aircraft_code  char(3),
                miles          int,
                departures     int,
                minutes        int,
                seats          int,
                passengers     int,
                freight_pounds int
            );
            """
        )
        self.redshift_client.execute_query(
            f"""
            COPY flights
            FROM 's3://us-west-2-aws-training/courses/spl-17/v4.2.15.prod-90ac2409/data/flights-usa'
            IAM_ROLE '{self.aws_iam_role}'
            GZIP
            DELIMITER ','
            REMOVEQUOTES
            REGION 'us-west-2';
            """
        )
        print("Tabela de flights criada.")

    def create_aircraft_table_copy_csv(self):
        self.redshift_client.execute_query(
            f"""
            CREATE TABLE aircraft (
                aircraft_code CHAR(3) SORTKEY,
                aircraft      VARCHAR(100)
            );
            """
        )
        self.redshift_client.execute_query(
            f"""
            COPY aircraft
            FROM 's3://us-west-2-aws-training/courses/spl-17/v4.2.15.prod-90ac2409/data/lookup_aircraft.csv'
            IAM_ROLE '{self.aws_iam_role}'
            IGNOREHEADER 1
            DELIMITER ','
            REMOVEQUOTES
            TRUNCATECOLUMNS
            REGION 'us-west-2';
            """
        )
        print("Tabela de aircraft criada.")

    def create_airports_table_copy_csv(self):
        self.redshift_client.execute_query(
            f"""
            CREATE TABLE airports (
                airport_code CHAR(3) SORTKEY,
                airport      varchar(100)
            );
            """
        )
        self.redshift_client.execute_query(
            f"""
            COPY airports
            FROM 's3://us-west-2-aws-training/courses/spl-17/v4.2.15.prod-90ac2409/data/lookup_airports.csv'
            IAM_ROLE '{self.aws_iam_role}'
            IGNOREHEADER 1
            DELIMITER ','
            REMOVEQUOTES
            TRUNCATECOLUMNS
            REGION 'us-west-2';
            """
        )
        print("Tabela de airports criada.")

    def create_view_only_las_vegas_destiny(self):
        self.redshift_client.execute_query(
            f"""
            CREATE VIEW vegas_flights AS
            SELECT 
                f.*,
                air.*
            FROM flights f 
            JOIN airports air ON f.origin = air.airport_code
            WHERE f.dest= 'LAS'
            """
        )
        print("View com voos de destino de Las Vegas criada.")
