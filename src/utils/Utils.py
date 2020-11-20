class Utils:

    @staticmethod
    def get_depth(element):
        depth = 0
        parent = element

        while parent is not None:
            parent = parent.parent
            depth += 1

        return depth

    @staticmethod
    def lowest_common_ancestor(first, second):
        first_parent = first
        while first_parent is not None:
            second_parent = second

            while second_parent is not None:
                if first_parent == second_parent:
                    return first_parent
                second_parent = second_parent.parent
            first_parent = first_parent.parent

        return None
