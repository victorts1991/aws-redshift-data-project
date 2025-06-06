from scenario_flights.redshift.redshift_ddl_dml_queries import RedshiftDdlDmlQueries
from scenario_flights.redshift.redshift_analysis_queries import RedshiftAnalysisQueries

class FlightsDataPipeline:

    def __init__(self, redshift_client, aws_iam_role):

        self.redshift_client = redshift_client
        self.aws_iam_role = aws_iam_role

    def run_pipeline(self):
        print("Starting AWS Redshift Flights Data Pipeline...")
        
        ddlDmlQueries = RedshiftDdlDmlQueries(
            self.redshift_client, 
            self.aws_iam_role
        )

        ddlDmlQueries.create_flights_table_copy_csv()
        ddlDmlQueries.create_aircraft_table_copy_csv()
        ddlDmlQueries.create_airports_table_copy_csv()
        ddlDmlQueries.create_view_only_las_vegas_destiny()

        print("Finish AWS Redshift Flights Data Pipeline...")
    
    def run_analysis_queries(self):
        print("Starting AWS Redshift Flights Analysis Queries...")

        analysisQueries = RedshiftAnalysisQueries(self.redshift_client)

        analysisQueries.analyze_count_how_many_flight_records()
        analysisQueries.analyze_which_top_10_aircraft_have_the_most_flights()
        analysisQueries.analyze_what_are_the_top_10_most_popular_flights_from_las_vegas()

        print("\nFinish AWS Redshift Flights Analysis Queries...")

    
