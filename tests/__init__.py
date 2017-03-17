from __future__ import absolute_import, division, print_function, unicode_literals

try:
    import std_msgs.msg as std_msgs
    import genpy
    import pyros_msgs.msg
except ImportError:
    # Because we need to access Ros message types here (from ROS env or from virtualenv, or from somewhere else)
    import pyros_setup
    # We rely on default configuration to point us to the proper distro
    pyros_setup.configurable_import().configure().activate()
    import std_msgs.msg as std_msgs
    import genpy
    import pyros_msgs.msg

import hypothesis
import hypothesis.strategies as st

import six
six_long = six.integer_types[-1]


def maybe_list(l):
    """Return list of one element if ``l`` is a scalar."""
    return l if l is None or isinstance(l, list) else [l]


# For now We use a set of basic messages for testing
std_msgs_dict_field_strat_ok = {
    # in python, booleans are integer type, but we dont want to test that here.
    'std_msgs/Bool': st.booleans(),
    'std_msgs/Int8': st.integers(min_value=-128, max_value=127),  # in python booleans are integers
    'std_msgs/Int16': st.integers(min_value=-32768, max_value=32767),
    'std_msgs/Int32': st.integers(min_value=-2147483648, max_value=2147483647),
    'std_msgs/Int64': st.integers(min_value=-six_long(9223372036854775808), max_value=six_long(9223372036854775807)),
    'std_msgs/UInt8': st.integers(min_value=0, max_value=255),
    'std_msgs/UInt16': st.integers(min_value=0, max_value=65535),
    'std_msgs/UInt32': st.integers(min_value=0, max_value=4294967295),
    'std_msgs/UInt64': st.integers(min_value=0, max_value=six_long(18446744073709551615)),
    'std_msgs/Float32': st.floats(min_value=-3.4028235e+38, max_value=3.4028235e+38),
    'std_msgs/Float64': st.floats(min_value=-1.7976931348623157e+308, max_value=1.7976931348623157e+308, ),
    'std_msgs/String': st.one_of(st.binary(), st.text(alphabet=st.characters(max_codepoint=127))),
    'std_msgs/Time':
        # only one way to build a python data for a time message
        st.integers(min_value=six_long(0), max_value=six_long(18446744073709551615)),
    'std_msgs/Duration':
        # only one way to build a python data for a duration message
        st.integers(min_value=-six_long(9223372036854775808), max_value=six_long(9223372036854775807)),
    # TODO : add more. we should test all.
}

std_msgs_types_strat_ok = {
    # in python, booleans are integer type, but we dont want to test that here.
    # Where there is no ambiguity, we can reuse std_msgs_dict_field_strat_ok strategies
    'std_msgs/Bool': st.builds(std_msgs.Bool, data=std_msgs_dict_field_strat_ok.get('std_msgs/Bool')),
    'std_msgs/Int8': st.builds(std_msgs.Int8, data=std_msgs_dict_field_strat_ok.get('std_msgs/Int8')),
    'std_msgs/Int16': st.builds(std_msgs.Int16, data=std_msgs_dict_field_strat_ok.get('std_msgs/Int16')),
    'std_msgs/Int32': st.builds(std_msgs.Int32, data=std_msgs_dict_field_strat_ok.get('std_msgs/Int32')),
    'std_msgs/Int64': st.builds(std_msgs.Int64, data=std_msgs_dict_field_strat_ok.get('std_msgs/Int64')),
    'std_msgs/UInt8': st.builds(std_msgs.UInt8, data=std_msgs_dict_field_strat_ok.get('std_msgs/UInt8')),
    'std_msgs/UInt16': st.builds(std_msgs.UInt16, data=std_msgs_dict_field_strat_ok.get('std_msgs/UInt16')),
    'std_msgs/UInt32': st.builds(std_msgs.UInt32, data=std_msgs_dict_field_strat_ok.get('std_msgs/UInt32')),
    'std_msgs/UInt64': st.builds(std_msgs.UInt64, data=std_msgs_dict_field_strat_ok.get('std_msgs/UInt64')),
    'std_msgs/Float32': st.builds(std_msgs.Float32, data=std_msgs_dict_field_strat_ok.get('std_msgs/Float32')),
    'std_msgs/Float64': st.builds(std_msgs.Float64, data=std_msgs_dict_field_strat_ok.get('std_msgs/Float64')),
    'std_msgs/String': st.builds(std_msgs.String, data=std_msgs_dict_field_strat_ok.get('std_msgs/String')),
    'std_msgs/Time': st.builds(std_msgs.Time, data=st.one_of(
        # different ways to build a genpy.time (check genpy code)
        st.builds(genpy.Time, secs=st.integers(min_value=0, max_value=4294967295), nsecs=st.integers(min_value=0, max_value=4294967295)),
        st.builds(genpy.Time, nsecs=st.integers(min_value=six_long(0), max_value=six_long(9223372036854775807))),
        st.builds(genpy.Time, secs=st.floats()),
    )),
    'std_msgs/Duration': st.builds(std_msgs.Duration, data=st.one_of(
        # different ways to build a genpy.duration (check genpy code)
        st.builds(genpy.Duration, secs=st.integers(min_value=-2147483648, max_value=2147483648), nsecs=st.integers(min_value=-2147483648, max_value=2147483648)),
        st.builds(genpy.Duration, nsecs=st.integers(min_value=six_long(0), max_value=six_long(9223372036854775807))),
        st.builds(genpy.Duration, secs=st.floats()),
    )),
    # TODO : add more. we should test all.
}

std_msgs_types_strat_broken = {
    # everything else...
    'std_msgs/Bool': st.builds(std_msgs.Bool, data=st.one_of(st.integers(), st.floats())),
    'std_msgs/Int8': st.builds(std_msgs.Int8, data=st.one_of(st.floats(), st.integers(min_value=127+1), st.integers(max_value=-128-1))),
    'std_msgs/Int16': st.builds(std_msgs.Int16, data=st.one_of(st.floats(), st.integers(min_value=32767+1), st.integers(max_value=-32768-1))),
    'std_msgs/Int32': st.builds(std_msgs.Int32, data=st.one_of(st.floats(), st.integers(min_value=2147483647+1), st.integers(max_value=-2147483648-1))),
    'std_msgs/Int64': st.builds(std_msgs.Int64, data=st.one_of(st.floats(), st.integers(min_value=six_long(9223372036854775807+1)), st.integers(max_value=six_long(-9223372036854775808-1)))),
    'std_msgs/UInt8': st.builds(std_msgs.UInt8, data=st.one_of(st.floats(), st.integers(min_value=255+1), st.integers(max_value=-1))),
    'std_msgs/UInt16': st.builds(std_msgs.UInt16, data=st.one_of(st.floats(), st.integers(min_value=65535+1), st.integers(max_value=-1))),
    'std_msgs/UInt32': st.builds(std_msgs.UInt32, data=st.one_of(st.floats(), st.integers(min_value=4294967295+1), st.integers(max_value=-1))),
    'std_msgs/UInt64': st.builds(std_msgs.UInt64, data=st.one_of(st.floats(), st.integers(min_value=six_long(18446744073709551615+1)), st.integers(max_value=-1))),
    'std_msgs/Float32': st.builds(std_msgs.Float32, data=st.one_of(st.booleans(), st.integers())),  # st.floats(max_value=-3.4028235e+38), st.floats(min_value=3.4028235e+38))),
    'std_msgs/Float64': st.builds(std_msgs.Float64, data=st.one_of(st.booleans(), st.integers())),  # st.floats(max_value=-1.7976931348623157e+308), st.floats(min_value=1.7976931348623157e+308))),
    # TODO : add more. we should test all
}


def proper_basic_strategy_selector(*msg_types):
    """Accept a (list of) rostype and return it with the matching strategy for ros message"""
    # TODO : break on error (type not in map)
    # we use a list comprehension here to avoid creating a generator (tuple comprehension)
    return tuple([(msg_type, std_msgs_types_strat_ok.get(msg_type)) for msg_type in msg_types])


def proper_basic_data_strategy_selector(*msg_types):
    """Accept a (list of) rostype and return it with the matching strategy for data"""
    # TODO : break on error (type not in map)
    # we use a list comprehension here to avoid creating a generator (tuple comprehension)
    return tuple([(msg_type, std_msgs_dict_field_strat_ok.get(msg_type)) for msg_type in msg_types])