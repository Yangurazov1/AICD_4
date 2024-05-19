#!/usr/bin/env python3

"""
Application main class. Shows text user interface for interactive dictionary.
"""

from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Header, Label, Input, RichLog
from rich.text import Text

from sset import SSet

FILENAME = "small-words.txt"


class SearcherApp(App):
    """A textual app to interactively search in dictionary"""

    sset = SSet(FILENAME)

    def compose(self) -> ComposeResult:
        """Returns application window"""
        yield Header(show_clock=True)
        yield Input(placeholder="Type a string, e.g. squire")
        yield RichLog(id="results")
        yield Label("Press Ctrl-C to exit")

    def on_mount(self) -> None:
        """Called when app starts"""
        # Give the input focus, so we can start typing
        self.query_one(Input).loading = True
        self.sset.load()
        self.query_one(Input).loading = False
        self.query_one(Input).focus()

    def on_input_changed(self, message: Input.Changed) -> None:
        """Handles a changed text message."""
        if message.value:
            self.query_one("#results", RichLog).loading = True
            self.lookup_word(message.value)
            self.query_one("#results", RichLog).loading = False
        else:
            # Clear results
            self.query_one("#results", RichLog).clear()

    @work(exclusive=True)
    async def lookup_word(self, substr: str) -> None:
        """Writes a list of words into results."""
        results = self.sset.search(substr)
        log = self.query_one("#results", RichLog)
        log.clear()
        for w in results:
            pos = w.find(substr)
            if pos == -1:
                # wrong, no substr in word
                log.write(Text.from_markup(f"[strike bold red]{w}"))
            else:
                n = len(substr)
                before = w[0:pos]
                word = w[pos:pos+n]
                after = w[pos+n:]
                markup = before + "[bold green]" + word + "[/]" + after
                log.write(Text.from_markup(markup))


if __name__ == "__main__":
    app = SearcherApp()
    app.run()
