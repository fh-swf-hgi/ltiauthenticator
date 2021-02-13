from lti import OutcomeRequest
from nbgrader.api import Gradebook, MissingEntry
from nbgrader.plugins import ExportPlugin, BasePlugin
import os.path

class MoodleExporter(ExportPlugin):

    def export(self, gradebook):
        # Create the connection to the database
        with Gradebook('sqlite:///gradebook.db') as gb:

            # Loop over each assignment in the database
            for assignment in gb.assignments:
                print("Exporting...")
                print("     Course-ID: " + assignment.course_id)
                print("     Assignment-Name: " + assignment.name)

                # Loop over each student in the database
                for student in gb.students:

                    # Check if file with lis-Parameters exists
                    path = (
                        '/srv/nbgrader/exchange/' + assignment.course_id + ''
                        '/inbound/log/' + assignment.name + ''
                        '/' + student.id + '.txt'
                    )

                    if os.path.isfile(path):
                        print("         Student-ID: " + student.id)

                        # Get stored parameters from the file
                        parameters = {}
                        with open(path, 'r') as log:
                            lines = log.read().splitlines()
                            parameters = {
                                'lis_outcome_service_url': lines[0],
                                'lis_result_sourcedid': lines[1]
                            }

                        # Try to find the submission in the database. If it doesn't exist, the
                        # `MissingEntry` exception will be raised, which means the student
                        # didn't submit anything, so we assign them a score of zero.
                        try:
                            submission = gb.find_submission(assignment.name, student.id)
                        except MissingEntry:
                            parameters['score'] = 0.0
                        else:
                            # Four digits shown in Moodle
                            resultscore = round(submission.score/assignment.max_score, 4)
                            if resultscore > 1:
                                resultscore = 1
                            parameters['score'] = resultscore

                        self.post_grades(parameters)

                    else:
                        print("         No LTI-Parameters found for: " + student.id)

    def post_grades(self, parameters):
        
        # Secret of the external Tool
        consumer_key = '5769a1a29a1b101ffdaa06048793c59b19b4c252eb651d03872048a30f8db283'
        consumer_secret = 'c732af9c6235cc8530d24bcab00a0e70704ac550cd0434a3d1a298e124bbd590'

        # Create POST-Request
        outcome_request = OutcomeRequest({
            'consumer_key': consumer_key,
            'consumer_secret': consumer_secret,
            'lis_outcome_service_url': parameters['lis_outcome_service_url'],
            'lis_result_sourcedid': parameters['lis_result_sourcedid']
        })

        # Replace result in Moodle
        outcome_response = outcome_request.post_replace_result(parameters['score'])
