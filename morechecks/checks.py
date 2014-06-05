from django.conf import settings, global_settings
from django.core import checks
from django.template import Template, Context
from django.test.client import RequestFactory
from django.utils.module_loading import import_string
from django.db import connection, reset_queries
from django.core.signals import request_started
from django.test.testcases import _AssertNumQueriesContext


def templates_do_not_do_queries(app_configs, **kwargs):
    # get only the processors that aren't defaults
    processors = set(settings.TEMPLATE_CONTEXT_PROCESSORS)
    base_processors = set(global_settings.TEMPLATE_CONTEXT_PROCESSORS)
    only_these_processors = processors - base_processors
    request = RequestFactory().get('/')
    issues = []

    # emulates .django.test.utils.CaptureQueriesContext.__enter__
    connection.use_debug_cursor = True
    request_started.disconnect(reset_queries)

    raw_msg = 'executed {{ count }} quer{{ count|pluralize:"y,ies" }}'
    msg_template = Template(raw_msg)
    for processor in only_these_processors:
        count_before = len(connection.queries)
        # fetch and execute the context processor.
        # emulates django.template.context.RequestContext.__init__
        import_string(processor)(request)
        count_after = len(connection.queries)
        if count_after > count_before:
            final_count = count_after - count_before
            msg = msg_template.render(Context({'count': final_count}))
            issues.append(
                checks.Warning(msg, obj=processor, id="morechecks.W001"))

    # emulates .django.test.utils.CaptureQueriesContext.__exit__
    connection.use_debug_cursor = False
    request_started.connect(reset_queries)
    return issues
