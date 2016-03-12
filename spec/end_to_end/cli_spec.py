import subprocess
import shutil

from expects import expect, equal, match

from linkstore.link_storage import ApplicationDataDirectory


def invoke_cli(*arguments):
    path_to_cli_binary = subprocess.check_output([ 'which', 'linkstore' ]).strip()

    try:
        output = subprocess.check_output(
            [ 'coverage', 'run', '--append' ] +
            [ path_to_cli_binary ] +
            list(arguments)
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


with description('the command-line application'):
    with context('when retrieving saved links'):
        with before.each:
            self.DATE_PATTERN = r'[0-9]{2}/[0-9]{2}/[0-9]{4}'
            self.NUMBER_AT_BEGINNING_OF_LINE_PATTERN = r'^\d+'

        with context('by tag'):
            with before.each:
                self.tag_filter = 'some_tag'
                links_to_save = [
                    ('some url',        self.tag_filter),
                    ('another url',     self.tag_filter),
                    ('yet another url', 'a_different_tag')
                ]

                for link in links_to_save:
                    invoke_cli('save', link[0], link[1])
                self.saved_links = links_to_save


                self.execution_result = invoke_cli('list', self.tag_filter)

            with it('does not fail'):
                expect(self.execution_result.exit_code).to(equal(0))

            with it('outputs a line per matching link'):
                number_of_lines_in_output = len(self.execution_result.lines_in_output)
                number_of_matching_links = len([ link for link in self.saved_links if link[1] == self.tag_filter ])

                expect(number_of_lines_in_output).to(equal(number_of_matching_links))

            with context('output lines'):
                with it('have an id'):
                    self.expect_output_lines_to_have_an_id()

                with it('have an URL'):
                    self.expect_output_lines_to_have_an_url()

                with it('have a date'):
                    self.expect_output_lines_to_have_a_date()

                with it('have no tags'):
                    for line_number, line in enumerate(self.execution_result.lines_in_output):
                        tag = self.saved_links[line_number][1]

                        expect(line).not_to(match(tag))
                        expect(line).not_to(match(self.tag_filter))

        def expect_output_lines_to_have_an_id(self):
            for line in self.execution_result.lines_in_output:
                expect(line).to(match(self.NUMBER_AT_BEGINNING_OF_LINE_PATTERN))

        def expect_output_lines_to_have_an_url(self):
            for line_number, line in enumerate(self.execution_result.lines_in_output):
                url = self.saved_links[line_number][0]
                expect(line).to(match(url))

        def expect_output_lines_to_have_a_date(self):
            for line in self.execution_result.lines_in_output:
                expect(line).to(match(self.DATE_PATTERN))

        with context('all saved links'):
            with before.each:
                links_to_save = [
                    ('some url',        ('a tag',)),
                    ('another url',     ('first tag', 'second tag')),
                    ('yet another url', ('a_different_tag',))
                ]

                for link in links_to_save:
                    invoke_cli('save', link[0], *link[1])
                self.saved_links = links_to_save

                self.execution_result = invoke_cli('list')

            with it('does not fail'):
                expect(self.execution_result.exit_code).to(equal(0))

            with it('outputs a line per saved link'):
                number_of_lines_in_output = len(self.execution_result.lines_in_output)
                number_of_saved_links = len(self.saved_links)

                expect(number_of_lines_in_output).to(equal(number_of_saved_links))

            with context('output lines'):
                with it('have an id'):
                    self.expect_output_lines_to_have_an_id()

                with it('have an URL'):
                    self.expect_output_lines_to_have_an_url()

                with it('have a date'):
                    self.expect_output_lines_to_have_a_date()

                with it('have the tags of the relevant link'):
                    for line_number, line in enumerate(self.execution_result.lines_in_output):
                        tags = self.saved_links[line_number][1]

                        for tag in tags:
                            expect(line).to(match(tag))

    with after.each:
        shutil.rmtree(ApplicationDataDirectory().path)
