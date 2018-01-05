from capturer import CaptureOutput
from fabric.tasks import WrappedCallableTask


class LoggedTask(WrappedCallableTask):
    capturing = [False]

    def run(self, *args, **kwargs):
        if self.capturing[0]:
            return super(LoggedTask, self).run(*args, **kwargs)

        with CaptureOutput() as capturer:
            self.capturing[0] = True

            try:
                task = super(LoggedTask, self).run(*args, **kwargs)
            finally:
                self.capturing[0] = False

        print "-" * 40
        print capturer.get_lines()

        return task


def logged_task(*args, **kwargs):
    """
    Decorator declaring the wrapped function to be a new-style task.

    May be invoked as a simple, argument-less decorator (i.e. ``@task``) or
    with arguments customizing its behavior (e.g. ``@task(alias='myalias')``).

    Please see the :ref:`new-style task <task-decorator>` documentation for
    details on how to use this decorator.

    .. versionchanged:: 1.2
        Added the ``alias``, ``aliases``, ``task_class`` and ``default``
        keyword arguments. See :ref:`task-decorator-arguments` for details.
    .. versionchanged:: 1.5
        Added the ``name`` keyword argument.

    .. seealso:: `~fabric.docs.unwrap_tasks`, `~fabric.tasks.WrappedCallableTask`
    """
    invoked = bool(not args or kwargs)
    task_class = kwargs.pop("task_class", LoggedTask)
    if not invoked:
        func, args = args[0], ()

    def wrapper(func):
        return task_class(func, *args, **kwargs)

    return wrapper if invoked else wrapper(func)
