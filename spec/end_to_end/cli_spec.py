import subprocess
import shutil

from expects import expect, equal, be_empty, match, have_length, contain

from linkstore.link_storage import ApplicationDataDirectory


def invoke_cli(arguments):
    path_to_cli_binary = subprocess.check_output([ 'which', 'linkstore' ]).strip()

    try:
        output = subprocess.check_output(
            [ 'coverage', 'run', '--append' ] +
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


with description('the command-line application'):
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
            self.DATE_PATTERN = r'[0-9]{2}/[0-9]{2}/[0-9]{4}'

        with context('by tag'):
            with before.each:
                self.tag_filter = 'some_tag'
                links_to_save = [
                    ('some url',        self.tag_filter),
                    ('another url',     self.tag_filter),
                    ('yet another url', 'a_different_tag')
                ]

                for link in links_to_save:
                    invoke_cli([ 'save', link[0], link[1] ])
                self.saved_links = links_to_save


                self.execution_result = invoke_cli([ 'list', self.tag_filter ])

            with it('does not fail'):
                expect(self.execution_result.exit_code).to(equal(0))

            with it('outputs a line per matching link'):
                number_of_lines_in_output = len(self.execution_result.lines_in_output)
                number_of_matching_links = len([ link for link in self.saved_links if link[1] == self.tag_filter ])

                expect(number_of_lines_in_output).to(equal(number_of_matching_links))

            with context('output lines'):
                with it('have an id'):
                    NUMBER_AT_BEGINNING_OF_LINE_PATTERN = r'^\d+'

                    for line in self.execution_result.lines_in_output:
                        expect(line).to(match(NUMBER_AT_BEGINNING_OF_LINE_PATTERN))

                with it('have an URL'):
                    for line_number, line in enumerate(self.execution_result.lines_in_output):
                        url = self.saved_links[line_number][0]
                        expect(line).to(match(url))

                with it('have a date'):
                    for line in self.execution_result.lines_in_output:
                        expect(line).to(match(self.DATE_PATTERN))

                with it('have no tags'):
                    for line_number, line in enumerate(self.execution_result.lines_in_output):
                        tag = self.saved_links[line_number][1]

                        expect(line).not_to(match(tag))
                        expect(line).not_to(match(self.tag_filter))

        with context('all saved links'):
            with before.each:
                links_to_save = [
                    ('some url',        ('a tag',)),
                    ('another url',     ('first tag', 'second tag')),
                    ('yet another url', ('a_different_tag',))
                ]

                for link in links_to_save:
                    invoke_cli([ 'save', link[0] ] + list(link[1]))
                self.saved_links = links_to_save

                self.execution_result = invoke_cli([ 'list' ])

            with it('does not fail'):
                expect(self.execution_result.exit_code).to(equal(0))

            with it('outputs a line per saved link'):
                number_of_lines_in_output = len(self.execution_result.lines_in_output)
                number_of_saved_links = len(self.saved_links)

                expect(number_of_lines_in_output).to(equal(number_of_saved_links))

            with it('outputs the URL and tags of each saved link per line'):
                for line_number, line in enumerate(self.execution_result.lines_in_output):
                    url, tags = self.saved_links[line_number]

                    expect(line).to(match(url))
                    expect(line).to(match(self.DATE_PATTERN))

                    for tag in tags:
                        expect(line).to(match(tag))

    with context('when re-tagging links'):
        with before.each:
            self.an_url = 'https://www.example.com/'
            self.old_tag = 'favourites'
            invoke_cli([ 'save', self.an_url, self.old_tag ])

            self.new_tag = 'not-so-favourites'
            self.execution_result = invoke_cli([ 'retag', '1' ] + [ self.old_tag, self.new_tag ])

        with it('does not fail'):
            expect(self.execution_result.exit_code).to(equal(0))

        with it('does not output anything'):
            expect(self.execution_result.lines_in_output).to(be_empty)

        with it('removes the old tag'):
            links_matching_old_tag = invoke_cli([ 'list', self.old_tag ]).lines_in_output

            expect(links_matching_old_tag).to(be_empty)

        with it('adds the new tag'):
            links_matching_new_tag = invoke_cli([ 'list', self.new_tag ]).lines_in_output

            expect(links_matching_new_tag).to(have_length(1))
            expect(links_matching_new_tag[0]).to(match(self.an_url))

    with context('when tagging links'):
        with before.each:
            self.an_url = 'https://www.example.com/'
            self.old_tag = 'favourites'
            invoke_cli([ 'save', self.an_url, self.old_tag ])

            self.some_new_tags = ('very-favourites', 'very-very-favourites', 'in-love-with-this-link')
            self.execution_result = invoke_cli([ 'tag', '1'] + list(self.some_new_tags))

        with it('does not fail'):
            expect(self.execution_result.exit_code).to(equal(0))

        with it('does not output anything'):
            expect(self.execution_result.lines_in_output).to(be_empty)

        with it('preserves the existing tag'):
            links_matching_old_tag = invoke_cli([ 'list', self.old_tag ]).lines_in_output

            expect(links_matching_old_tag).to(contain(match(self.an_url)))

        with it('adds the requested tag'):
            for new_tag in self.some_new_tags:
                links_matching_new_tag = invoke_cli([ 'list', new_tag ]).lines_in_output

                expect(links_matching_new_tag).to(contain(match(self.an_url)))

    with after.each:
        shutil.rmtree(ApplicationDataDirectory().path)
