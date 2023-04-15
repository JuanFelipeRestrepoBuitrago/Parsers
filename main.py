from top_down_parser import tests_t_d
from bottom_up_parser import tests_b_u


def top_down_parser():
    # tests_t_d.test_grammar()
    # tests_t_d.test_first()
    # tests_t_d.test_follow()
    # tests_t_d.test_check_ll1()
    tests_t_d.test_table()
    # tests_t_d.test_parser()
    # tests_t_d.final_test()


def bottom_up_parser():
    # tests_b_u.test_closure()
    # tests_b_u.test_goto()
    # tests_b_u.test_states()
    # tests_b_u.test_action()
    # tests_b_u.test_print_table()
    # tests_b_u.test_parser()
    tests_b_u.test_final()


if __name__ == "__main__":
    top_down_parser()
    # bottom_up_parser()
