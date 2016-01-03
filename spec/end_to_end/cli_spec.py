import subprocess
import shutil

from expects import expect, equal, be_empty, match
from ..helpers import have_the_same_length_as

from linkstore.link_storage import ApplicationDataDirectory


def invoke_cli(arguments):
    path_to_cli_binary = subprocess.check_output([ 'which', 'linkstore' ]).strip()

    try:
        output = subprocess.check_output(
            [ 'coverage', 'run', '--append', '--rcfile=.coveragerc_end-to-end' ] +
            [ path_to_cli_binary ] +
            arguments
        )
    except subprocess.CalledProcessError as error:
        return ExecutionResult(error.output, error.returncode)

    return ExecutionResult(output)

class ExecutionResult(object):
    def __init__(self, output, exit_code=0):
        self.lines_in_output = self._get_lines_from(output)
        self.exit_code = exit_code

    def _get_lines_from(self, output):
        if output == '':
            return []
        return output.strip().split('\n')


with description('the command-line interface'):
    with context('when saving links'):
        with before.each:
            self.an_url = 'https://www.example.com/'

        with context('without a tag'):
            with it('fails'):
                execution_result = invoke_cli([ 'save', self.an_url ])

                expect(execution_result.exit_code).not_to(equal(0))

        with context('with one tag'):
            with it('does not output anything'):
                a_tag = 'favourites'

                execution_result = invoke_cli([ 'save', self.an_url, a_tag ])

                expect(execution_result.exit_code).to(equal(0))
                expect(execution_result.lines_in_output).to(be_empty)

        with context('with more than one tag'):
            with it('does not output anything'):
                a_tag = 'favourites'
                another_tag = 'another_tag'

                execution_result = invoke_cli([ 'save', self.an_url, a_tag, another_tag ])

                expect(execution_result.exit_code).to(equal(0))
                expect(execution_result.lines_in_output).to(be_empty)


    with context('when retrieving saved links'):
        with before.each:
            self.DATE_REGEXP = r'[0-9]{2}/[0-9]{2}/[0-9]{4}'

        with context('by tag'):
            with it('outputs a line per retrieved link, containing the URL'):
                tag_filter = 'some_tag'
                links_to_save = [
                    ('some url',        tag_filter),
                    ('another url',     tag_filter),
                    ('yet another url', 'a_different_tag')
                ]

                for link in links_to_save:
                    invoke_cli([ 'save', link[0], link[1] ])


                execution_result = invoke_cli([ 'list', tag_filter ])


                expect(execution_result.exit_code).to(equal(0))

                number_of_lines_in_output = len(execution_result.lines_in_output)
                number_of_matching_links = len([ link for link in links_to_save if link[1] == tag_filter ])
                expect(number_of_lines_in_output).to(equal(number_of_matching_links))

                for line_number, line in enumerate(execution_result.lines_in_output):
                    url_of_current_link, tag_of_current_link = links_to_save[line_number]

                    expect(line).to(match(url_of_current_link))
                    expect(line).to(match(self.DATE_REGEXP))
                    expect(line).not_to(match(tag_of_current_link))
                    expect(line).not_to(match(tag_filter))

        with context('all saved links'):
            with it('outputs a line per retrieved link, containing its URL and tags'):
                links_to_save = [
                    ('some url',        ('a tag',)),
                    ('another url',     ('first tag', 'second tag')),
                    ('yet another url', ('a_different_tag',))
                ]

                for link in links_to_save:
                    invoke_cli([ 'save', link[0] ] + list(link[1]))

                execution_result = invoke_cli([ 'list' ])

                expect(execution_result.exit_code).to(equal(0))
                expect(execution_result.lines_in_output).to(have_the_same_length_as(links_to_save))

                for line_number, line in enumerate(execution_result.lines_in_output):
                    url_of_current_link, tags_of_current_link = links_to_save[line_number]

                    expect(line).to(match(url_of_current_link))
                    expect(line).to(match(self.DATE_REGEXP))

                    for tag in tags_of_current_link:
                        expect(line).to(match(tag))


    with after.each:
        shutil.rmtree(ApplicationDataDirectory().path)
