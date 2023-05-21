from top_down_parser import tests_t_d
from bottom_up_parser import tests_b_u


def top_down_parser():
    # tests_t_d.test_grammar()
    # tests_t_d.test_first()
    # tests_t_d.test_follow()
    # tests_t_d.test_check_ll1()
    # tests_t_d.test_table()
    # tests_t_d.test_parser()
    tests_t_d.final_test()


def bottom_up_parser():
    # tests_b_u.test_closure()
    # tests_b_u.test_goto()
    # tests_b_u.test_states()
    # tests_b_u.test_action()
    # tests_b_u.test_print_table()
    # tests_b_u.test_parser()
    tests_b_u.test_final()


if __name__ == "__main__":
    while True:
        print("Main Menu")
        print("1. Access to Top-Down")
        print("2. Access to Bottom-Up")
        print("0. Exit")

        option = input("Choose an option: ")
        print()

        if option == "1":
            top_down_parser()
        elif option == "2":
            bottom_up_parser()
        elif option == "0":
            print("Exiting...")
            break
        else:
            print("Invalid option, try again")
        print()
