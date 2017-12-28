from PageElement import PageElement
from NavigableString import NavigableString

EMPTY_ELEMENTS = ["area", "input", "textarea"]


class Tag(PageElement):
    def __init__(self, name,  attrs=None, parent=None, previous_sibling=None):
        PageElement.__init__(self, parent, previous_sibling)
        self.name = name
        if attrs is None:
            attrs = {}
        self.attrs = attrs
        self.contents = []

    def index(self, element):
        """
        Find the index of a child by identity, not value. Avoids issues with
        tag.contents.index(element) getting the index of equal elements.
        """
        for i, child in enumerate(self.contents):
            if child is element:
                return i
        raise ValueError("Tag.index: element not in tag")

    def append_f(self, new_child):
        if new_child is None:
            raise ValueError("Cannot append None to a tag.")
        if not isinstance(new_child, PageElement) and not isinstance(new_child, str):
            raise TypeError("Inserted only takes objects of type Tag, NavigableString, or str as second parameter.")
        if new_child is self:
            raise ValueError("Cannot append a tag to itself.")
        if isinstance(new_child, str) and not isinstance(new_child, NavigableString):
            new_child = NavigableString(new_child)



    # use when it is known that new_child is a PageElement object, has no parent (and thus is not
    # present in the contents of self), has no siblings, and is not self.
    def _append_f(self, new_child):
        try:
            self.contents[-1].next_sibling = new_child
            new_child.previous_sibling = self.contents[-1]
        # if len(contents) == 0
        except IndexError:
            pass
        new_child.parent = self
        self.contents.append(new_child)

        return new_child

    def insert(self, position, new_child):
        if new_child is None:
            raise ValueError("Cannot insert None into a tag.")
        if not isinstance(new_child, PageElement) and not isinstance(new_child, str):
            raise TypeError("Inserted only takes objects of type Tag, NavigableString, or str as second parameter.")
        if new_child is self:
            raise ValueError("Cannot insert a tag into itself.")
        if isinstance(new_child, str) and not isinstance(new_child, NavigableString):
            new_child = NavigableString(new_child)

        # If new_child has a parent, extract new_child.
        if hasattr(new_child, 'parent') and new_child.parent is not None:
            # If inserting an element that is a child of self,
            if new_child.parent is self:
                # the index of new_child in self.contents
                current_index = self.index(new_child)
                # if position is greater than the length of self.contents
                # todo: is there a better O(1) way to do this?
                try:
                    self.contents[position]
                except IndexError:
                    extracted_child = self._extract_f(current_index)
                    return self._append_f(extracted_child)

                # if new_child is present before position
                if current_index < position:
                    extracted_child = self._extract_f(current_index)
                    position -= 1

                    return self._insert_f(position, extracted_child)

        # a more efficient way O(1) vs. O(n) of saying
        # if position >= len(self.contents): position = len(self.contents)
        try:
            self.contents[position]
        except IndexError:
            return self._append_f(new_child)

        return self._insert(position, new_child)

    # use when it is known that new_child is a PageElement object, has no parent (and thus is not
    # present in the contents of self), has no siblings, and is not self. it must also be
    # known that position <= len(self.contents)
    def _insert(self, position, new_child):
        if position != 0:
            self.contents[position - 1].next_sibling = new_child
            new_child.previous_sibling = self.contents[position - 1]
        new_child.next_sibling = self.contents[position]
        self.contents[position].previous_sibling = new_child
        self.contents.insert(position, new_child)
        return new_child

    # def insert(self, position, new_child):
    #     if new_child is None:
    #         raise ValueError("Cannot insert None into a tag.")
    #     if new_child is self:
    #         raise ValueError("Cannot insert a tag into itself.")
    #     if isinstance(new_child, str) and not isinstance(new_child, NavigableString):
    #         new_child = NavigableString(new_child)
    #
    #     position = min(position, len(self.contents))
    #     # if new_child has a parent, extract it.
    #     if hasattr(new_child, 'parent') and new_child.parent is not None:
    #         # If we're 'inserting' an element that's already one
    #         # of this object's children.
    #         if new_child.parent is self:
    #             current_index = self.index(new_child)
    #             if current_index < position:
    #                 del self.contents[current_index]
    #
    #                 # We're moving this element further down the list
    #                 # of this object's children. That means that when
    #                 # we extract this element, our target index will
    #                 # jump down one.
    #                 position -= 1
    #         new_child.extract()
    #
    #     new_child.parent = self
    #     if position == 0:
    #         new_child.previous_sibling = None
    #         new_child.previous_element = self
    #     else:
    #         previous_child = self.contents[position - 1]
    #         new_child.previous_sibling = previous_child
    #         new_child.previous_sibling.next_sibling = new_child
    #         new_child.previous_element = previous_child._last_descendant(False)
    #     if new_child.previous_element is not None:
    #         new_child.previous_element.next_element = new_child
    #
    #     new_child_last_element = new_child._last_descendant(False)
    #
    #     if position >= len(self.contents):
    #         new_child.next_sibling = None
    #
    #         parent = self
    #         parents_next_sibling = None
    #         while parents_next_sibling is None and parent is not None:
    #             parents_next_sibling = parent.next_sibling
    #             parent = parent.parent
    #             if parents_next_sibling is not None:
    #                 # We found the element that comes next in the document.
    #                 break
    #         if parents_next_sibling is not None:
    #             new_child_last_element.next_element = parents_next_sibling
    #         else:
    #             # The last element of this tag is the last element in
    #             # the document.
    #             new_child_last_element.next_element = None
    #     else:
    #         next_child = self.contents[position]
    #         new_child.next_sibling = next_child
    #         if new_child.next_sibling is not None:
    #             new_child.next_sibling.previous_sibling = new_child
    #         new_child_last_element.next_element = next_child
    #
    #     if new_child_last_element.next_element is not None:
    #         new_child_last_element.next_element.previous_element = new_child_last_element
    #     self.contents.insert(position, new_child)
    #
    # def _last_descendant(self, is_initialized=True, accept_self=True):
    #     """Finds the last element beneath this object to be parsed."""
    #     if is_initialized and self.next_sibling:
    #         last_child = self.next_sibling.previous_element
    #     else:
    #         last_child = self
    #         while isinstance(last_child, Tag) and last_child.contents:
    #             # set last_child to the last element in last_child's contents
    #             last_child = last_child.contents[-1]
    #     if not accept_self and last_child is self:
    #         last_child = None
    #     return last_child

    def append(self, tag):
        """Appends the given tag to the contents of this tag."""
        self.insert(len(self.contents), tag)

    def unwrap(self):
        my_parent = self.parent
        if not self.parent:
            raise ValueError("Cannot replace an element with its contents when that element is not part of a tree.")
        my_index = self.parent.index(self)
        self.extract()
        for child in reversed(self.contents[:]):
            my_parent.insert(my_index, child)
        return self

    @property
    def string(self):
        """Convenience property to get the single string within this tag.

        :Return: If this tag has a single string child, return value
         is that string. If this tag has no children, or more than one
         child, return value is None. If this tag has one child tag,
         return value is the 'string' attribute of the child tag,
         recursively.
        """
        if len(self.contents) != 1:
            return None
        child = self.contents[0]
        if isinstance(child, NavigableString):
            return child
        return child.string

    @string.setter
    def string(self, string):
        """
        Basically JS's node.innerText =
        :param string: string to replace with
        """
        for element in self.contents[:]:
            element.extract()
        self.append(string)

    def decode_contents(self, indent_level=None):
        """
        Returns the contents of a Tag as a string
        """
        s = []
        for c in self:
            text = None
            if isinstance(c, NavigableString):
                # text = c.output_ready(formatter)
                text = c.value
            elif isinstance(c, Tag):
                # recurse here
                s.append(c.decode(indent_level))
            if text and not self.name == 'pre':
                text = text.strip()
            if text:
                if indent_level is not None and not self.name == 'pre':
                    s.append(" " * (indent_level - 1))
                s.append(text)
                if not self.name == 'pre':
                    s.append("\n")
        return ''.join(s)

    def __iter__(self):
        """Iterating over a tag iterates over its contents."""
        return iter(self.contents)

    def decode(self, indent_level=None):
        attrs = []
        if self.attrs:
            for i in attrs:
                attrs.append(i[0] + '=' + i[1])

        close = ''
        close_tag = ''

        if self.name in EMPTY_ELEMENTS:
            close = '/'
        else:
            close_tag = '</%s>' % self.name

        should_pretty_print = self.name not in {'pre', 'textarea'} and indent_level is not None

        if should_pretty_print:
            contents = self.decode_contents(indent_level + 1)
        else:
            contents = self.decode_contents()

        result_string = ''
        attribute_string = ''
        if attrs:
            attribute_string = ' ' + ' '.join(attrs)
        if indent_level is not None:
            indent_space = ' ' * (indent_level - 1)
            result_string += indent_space
        result_string += '<%s%s%s>' % (self.name, attribute_string, close)
        if should_pretty_print:
            result_string += "\n"
        result_string += contents
        if should_pretty_print and contents and contents[-1] != "\n":
            result_string += "\n"
        if should_pretty_print and close_tag:
            result_string += indent_space
        result_string += close_tag

        if indent_level is not None and close_tag and self.next_sibling:
            result_string += "\n"
        return result_string

    def __str__(self):
        return self.decode()
