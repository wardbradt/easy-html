class PageElement:

    # taken from BS4's setup method
    def __init__(self, parent=None, previous_element=None, next_element=None, previous_sibling=None, next_sibling=None):
        """Sets up the initial relations between this element and
        other elements."""
        self.parent = parent

        self.previous_element = previous_element
        if previous_element is not None:
            self.previous_element.next_element = self

        self.next_element = next_element
        if self.next_element:
            self.next_element.previous_element = self

        self.next_sibling = next_sibling
        if self.next_sibling:
            self.next_sibling.previous_sibling = self

        if not previous_sibling and self.parent is not None and self.parent.contents:
            previous_sibling = self.parent.contents[-1]

        self.previous_sibling = previous_sibling
        if previous_sibling:
            self.previous_sibling.next_sibling = self

    def replace_with(self, replacement):
        if not self.parent:
            raise ValueError("Cannot replace one element with another when the element to be replaced is not part of "
                             "a tree.")
        if replacement is self:
            return
        if replacement is self.parent:
            raise ValueError("Cannot replace an element with its parent.")
        old_parent = self.parent
        my_index = self.parent.index(self)
        self.extract()
        old_parent.insert(my_index, replacement)
        return self

    def wrap(self, wrapper_tag):
        me = self.replace_with(wrapper_tag)
        wrapper_tag.append(me)
        return wrapper_tag

    def extract(self):
        """Destructively rips this element out of the tree."""
        if self.parent is not None:
            del self.parent.contents[self.parent.index(self)]

        # Find the two elements that would be next to each other if this element (and any children) hadn't been parsed.
        # Connect the two.
        last_child = self._last_descendant()
        next_element = last_child.next_element

        # todo: what is the second part of this conditional checking?
        if self.previous_element is not None and self.previous_element is not next_element:
            self.previous_element.next_element = next_element
        if next_element is not None and next_element is not self.previous_element:
            next_element.previous_element = self.previous_element
        self.previous_element = None
        last_child.next_element = None

        self.parent = None
        if self.previous_sibling is not None and self.previous_sibling is not self.next_sibling:
            self.previous_sibling.next_sibling = self.next_sibling
        if self.next_sibling is not None and self.next_sibling is not self.previous_sibling:
            self.next_sibling.previous_sibling = self.previous_sibling
        self.previous_sibling = self.next_sibling = None
        return self

    # abstract method - implement in child
    def _last_descendant(self, is_initialized=True, accept_self=True):
        return self

    def insert_before(self, predecessor):
        """Makes the given element the immediate predecessor of this one.

        The two elements will have the same parent, and the given element
        will be immediately before this one.
        """
        if self is predecessor:
            raise ValueError("Can't insert an element before itself.")
        parent = self.parent
        if parent is None:
            raise ValueError(
                "Element has no parent, so 'before' has no meaning.")
        # Extract first so that the index won't be screwed up if they
        # are siblings.
        if isinstance(predecessor, PageElement):
            predecessor.extract()
        index = parent.index(self)
        parent.insert(index, predecessor)

    def insert_after(self, successor):
        """Makes the given element the immediate successor of this one.

        The two elements will have the same parent, and the given element
        will be immediately after this one.
        """
        if self is successor:
            raise ValueError("Can't insert an element after itself.")
        parent = self.parent
        if parent is None:
            raise ValueError(
                "Element has no parent, so 'after' has no meaning.")
        # Extract first so that the index won't be screwed up if they
        # are siblings.
        if isinstance(successor, PageElement):
            successor.extract()
        index = parent.index(self)
        parent.insert(index+1, successor)

    # find methods (using name, attrs, and text) go here. They were deleted b/c they are unnecessary.
