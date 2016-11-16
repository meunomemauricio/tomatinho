
import sys

from unittest.mock import Mock
from gi.repository import GLib
from pytest import fixture

sys.path.append('src')
from tomatinho.state_timer import StateTimer  # noqa: E402


RUN_TIMEOUT = 5


@fixture
def main_loop():
    loop = GLib.MainLoop()
    timeout = GLib.Timeout(RUN_TIMEOUT)
    timeout.set_callback(lambda loop: loop.quit(), loop)
    timeout.attach()
    return loop


class TestStateTimer:

    def test_starting_timer(self, main_loop):
        """Make sure the timer runs the callback function."""
        mock = Mock()
        st = StateTimer()

        st.start(1, mock)
        main_loop.run()

        mock.assert_called_once_with()

    def test_restarting_timer(self, main_loop):
        """Restart the timer before it timeouts.

        Asserts that the callback function is not executed twice.
        """
        mock = Mock()
        st = StateTimer()
        st.start(1, mock)

        st.start(1, mock)
        main_loop.run()

        mock.assert_called_once_with()

    def test_stop_timer(self, main_loop):
        """Stop the timer before it timeouts.

        Asserts that the callback function is not executed.
        """
        mock = Mock()
        st = StateTimer()
        st.start(1, mock)

        st.stop()
        main_loop.run()

        mock.assert_not_called()

    def test_timer_does_not_loop(self, main_loop):
        """Timer does not run the same function more than once.

        Setting the Mock ``side_effect`` to True makes sure that the callback
        function is not passed directly to the ``GLib.timeout_add`` function.
        Otherwise there is the risk that a function returning something that
        evaluates to True might loop the timer.
        """
        mock = Mock(side_effect=True)
        st = StateTimer()

        st.start(1, mock)
        main_loop.run()

        mock.assert_called_once_with()
