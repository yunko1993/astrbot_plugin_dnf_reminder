import importlib
import sys
import tempfile
import types
import unittest


class FakeJob:
    def __init__(self, job_id):
        self.id = job_id


class FakeScheduler:
    def __init__(self, event_loop=None):
        self.event_loop = event_loop
        self.jobs = {}
        self.started = False
        self.shutdown_called = False

    def start(self):
        self.started = True

    def shutdown(self, wait=False):
        self.shutdown_called = True
        self.jobs.clear()

    def get_jobs(self):
        return list(self.jobs.values())

    def add_job(self, func, trigger, hour, minute, args, id, replace_existing):
        if not replace_existing and id in self.jobs:
            raise RuntimeError("duplicate job")
        self.jobs[id] = FakeJob(id)

    def remove_job(self, job_id):
        self.jobs.pop(job_id, None)


class FakeContext:
    def __init__(self):
        self.loop = object()
        self.scheduler = None

    def get_event_loop(self):
        return self.loop

    def get_scheduler(self):
        return self.scheduler


class Star:
    def __init__(self, context):
        self.context = context


class Context:
    pass


class AstrMessageEvent:
    pass


class Plain:
    def __init__(self, text=""):
        self.text = text


def passthrough_decorator(*args, **kwargs):
    def decorate(value):
        return value

    return decorate


def install_import_stubs():
    async_mod = types.ModuleType("apscheduler.schedulers.asyncio")
    async_mod.AsyncIOScheduler = FakeScheduler
    schedulers_mod = types.ModuleType("apscheduler.schedulers")
    apscheduler_mod = types.ModuleType("apscheduler")

    all_mod = types.ModuleType("astrbot.api.all")
    all_mod.register = passthrough_decorator
    all_mod.command = passthrough_decorator
    all_mod.Star = Star
    all_mod.Context = Context
    all_mod.AstrMessageEvent = AstrMessageEvent
    all_mod.Plain = Plain

    api_mod = types.ModuleType("astrbot.api")
    astrbot_mod = types.ModuleType("astrbot")

    sys.modules.update(
        {
            "apscheduler": apscheduler_mod,
            "apscheduler.schedulers": schedulers_mod,
            "apscheduler.schedulers.asyncio": async_mod,
            "astrbot": astrbot_mod,
            "astrbot.api": api_mod,
            "astrbot.api.all": all_mod,
        }
    )


def import_plugin_module():
    install_import_stubs()
    sys.modules.pop("main", None)
    return importlib.import_module("main")


class SchedulerLifecycleTest(unittest.TestCase):
    def test_external_scheduler_sync_clears_fallback_jobs(self):
        plugin_module = import_plugin_module()
        original_resolve_data_dir = plugin_module.PersonalReminder._resolve_data_dir

        with tempfile.TemporaryDirectory() as temp_dir:
            plugin_module.PersonalReminder._resolve_data_dir = lambda self: temp_dir
            try:
                context = FakeContext()
                plugin = plugin_module.PersonalReminder(
                    context,
                    config={
                        "configured_reminders": [
                            {
                                "enabled": True,
                                "time": "22:00",
                                "content": "领取心悦",
                                "targets": ["123456"],
                            }
                        ]
                    },
                )
            finally:
                plugin_module.PersonalReminder._resolve_data_dir = original_resolve_data_dir

        fallback_scheduler = plugin._fallback_scheduler
        self.assertIsNotNone(fallback_scheduler)
        self.assertEqual(
            [plugin_module.PLUGIN_ID + "_0"],
            [job.id for job in fallback_scheduler.get_jobs()],
        )

        external_scheduler = FakeScheduler()
        context.scheduler = external_scheduler

        plugin._ensure_scheduler_ready(force=True)

        self.assertEqual(
            [plugin_module.PLUGIN_ID + "_0"],
            [job.id for job in external_scheduler.get_jobs()],
        )
        self.assertEqual([], [job.id for job in fallback_scheduler.get_jobs()])
        self.assertTrue(fallback_scheduler.shutdown_called)


if __name__ == "__main__":
    unittest.main()
