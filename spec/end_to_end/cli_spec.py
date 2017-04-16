import subprocess
import shutil

from expects import expect, equal, match, contain

from linkstore.links import ApplicationDataDirectory


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
    with context('retrieving saved links'):
        with it('by tag'):
            self.tag_filter = 'some_tag'
            links_to_save = [
                ('some url',        (self.tag_filter, 'a second tag')),
                ('another url',     ('a third tag', self.tag_filter)),
                ('yet another url', ('a_different_tag',))
            ]
            for link in links_to_save:
                invoke_cli('save', link[0], *link[1])
            self.saved_links = links_to_save


            self.execution_result = invoke_cli('list', self.tag_filter)


            expect(self.execution_result.exit_code).to(equal(0))
            self.expect_output_lines_to_have_a_handle()
            self.expect_output_lines_to_have_an_url()
            self.expect_output_lines_to_have_a_date()
            self.expect_output_lines_to_not_have_tags()
            self.expect_output_to_have_a_line_per_matching_link()

        with it('all saved links'):
            links_to_save = [
                ('some url',        ('a tag',)),
                ('another url',     ('first tag', 'second tag')),
                ('yet another url', ('a_different_tag',))
            ]
            for link in links_to_save:
                invoke_cli('save', link[0], *link[1])
            self.saved_links = links_to_save


            self.execution_result = invoke_cli('list')


            expect(self.execution_result.exit_code).to(equal(0))
            self.expect_output_lines_to_have_a_handle()
            self.expect_output_lines_to_have_an_url()
            self.expect_output_lines_to_have_a_date()
            self.expect_output_to_have_a_line_per_saved_link()
            self.expect_output_to_have_all_tags_of_each_link()


        def expect_output_lines_to_have_a_handle(self):
            NUMBER_AT_BEGINNING_OF_LINE_PATTERN = r'^\d+'

            for line in self.execution_result.lines_in_output:
                expect(line).to(match(NUMBER_AT_BEGINNING_OF_LINE_PATTERN))

        def expect_output_lines_to_have_an_url(self):
            for line_number, line in enumerate(self.execution_result.lines_in_output):
                url = self.saved_links[line_number][0]
                expect(line).to(contain(url))

        def expect_output_lines_to_have_a_date(self):
            DATE_PATTERN = r'[0-9]{2}/[0-9]{2}/[0-9]{4}'

            for line in self.execution_result.lines_in_output:
                expect(line).to(match(DATE_PATTERN))

        def expect_output_lines_to_not_have_tags(self):
            for line_number, line in enumerate(self.execution_result.lines_in_output):
                tags = self.saved_links[line_number][1]

                for tag in tags:
                    expect(line).not_to(contain(tag))

                expect(line).not_to(contain(self.tag_filter))

        def expect_output_to_have_a_line_per_matching_link(self):
            number_of_lines_in_output = len(self.execution_result.lines_in_output)
            number_of_matching_links = len([ link for link in self.saved_links if self.tag_filter in link[1] ])

            expect(number_of_lines_in_output).to(equal(number_of_matching_links))

        def expect_output_to_have_a_line_per_saved_link(self):
            number_of_lines_in_output = len(self.execution_result.lines_in_output)
            number_of_saved_links = len(self.saved_links)

            expect(number_of_lines_in_output).to(equal(number_of_saved_links))

        def expect_output_to_have_all_tags_of_each_link(self):
            for line_number, line in enumerate(self.execution_result.lines_in_output):
                tags = self.saved_links[line_number][1]

                for tag in tags:
                    expect(line).to(contain(tag))


    with after.each:
        shutil.rmtree(ApplicationDataDirectory().path)
