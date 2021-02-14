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

    @staticmethod
    def clean(string):
        try:
            string = string.replace("\xa08", "8")
            string = string.replace("r\xa0", " ")
            string = string.replace("\xa0", " ")
            string = string.replace(u"\xa0", u" ")
            string = string.replace(u"\\xa0", u" ")
            string = string.replace(r'\n', '')
            string = string.replace("\n", '')
            string = string.replace(r'\t', '')
            string = string.replace("\t", '')
            # string = string.replace('\xa', '')
            return string.strip(" '")
        except TypeError:
            return ""

    @staticmethod
    def getCSSPath(element):
        return Utils.__get_css_path(element)

    @staticmethod
    def __get_element(node):
        # for XPATH we have to count only for nodes with same type!
        length = 1
        for sibling in node.previous_siblings:
            if sibling.name == node.name:
                length += 1
        if (length) > 1:
            return '%s:nth-of-type(%s)' % (node.name, length)
        else:
            return node.name

    @staticmethod
    def __get_css_path(node):
        path = [Utils.__get_element(node)]
        for parent in node.parents:
            if parent.name == 'body':
                break
            path.insert(0, Utils.__get_element(parent))
        return "html > body > " + (' > '.join(path))
