import re

from bs4 import NavigableString


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
            string = string.replace("\r", '')
            string = string.replace(r'\t', '')
            string = string.replace("\t", '')
            string = re.sub(' +', ' ', string)
            # string = string.replace('\xa', '')
            return string.strip(" ':")
        except TypeError:
            return ""

    @staticmethod
    def get_first_line(string):
        splitted = string.split("\n")
        for line in splitted:
            if Utils.clean(line) != "":
                return line

        return string

    @staticmethod
    def getTag(element):
        if isinstance(element, NavigableString):
            return element.parent

        return element

    @staticmethod
    def getCustomId(element):
        # this is workaround for NavigableString because it does not have assigned custom_id
        if isinstance(element, NavigableString) and element.parent is not None and element.parent.custom_id is not None:
            element.custom_id = 100000 + element.parent.custom_id

        try:
            return element.custom_id
        except AttributeError:
            return repr(element)

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
