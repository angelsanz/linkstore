import subprocess
import shutil

from expects import expect, equal, be_empty, match

from linkstore.link_storage import SqliteLinkStorage


def invoke_cli(arguments):
    path_to_cli_binary = subprocess.check_output([ 'which', 'linkstore' ]).strip()

    return ExecutionResult(
        subprocess.check_output(
            [ 'coverage', 'run', '--append', '--rcfile=.coveragerc_end-to-end' ] +
            [ path_to_cli_binary ] +
            arguments
        )
    )

class ExecutionResult(object):
    def __init__(self, output):
        self.lines_in_output = self._get_lines_from(output)
        self.exit_code = 0

    def _get_lines_from(self, output):
        if output == '':
            return []
        return output.strip().split('\n')


with description('the command-line interface'):
    with context('when saving links'):
        with it('does not output anything'):
            an_url = 'https://www.example.com/'
            a_tag = 'favourites'

            execution_result = invoke_cli([ 'save', an_url, a_tag ])

            expect(execution_result.exit_code).to(equal(0))
            expect(execution_result.lines_in_output).to(be_empty)

    with context('when retrieving links by tag'):
        with it('outputs a line per retrieved link'):
            tag_filter = 'some_tag'
            links_to_save = [
                ('some url',        tag_filter),
                ('another url',     tag_filter),
                ('yet another url', 'a_different_tag')
            ]

            for link in links_to_save:
                res = invoke_cli([ 'save', link[0], link[1] ])


            execution_result = invoke_cli([ 'list', tag_filter ])


            expect(execution_result.exit_code).to(equal(0))

            number_of_lines_in_output = len(execution_result.lines_in_output)
            number_of_matching_links = len([ link for link in links_to_save if link[1] == tag_filter ])
            expect(number_of_lines_in_output).to(equal(number_of_matching_links))

            for line_number in range(number_of_lines_in_output):
                line = execution_result.lines_in_output[line_number]
                url_of_current_link, tag_of_current_link = links_to_save[line_number]

                expect(line).to(match(url_of_current_link))
                expect(line).not_to(match(tag_of_current_link))
                expect(line).not_to(match(tag_filter))

    with after.each:
        shutil.rmtree(SqliteLinkStorage.PATH_TO_DATA_DIRECTORY)
