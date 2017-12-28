class PageElement:

    # taken from BS4's setup method
    def __init__(self, parent=None, previous_sibling=None, next_sibling=None):
        """Sets up the initial relations between this element and
        other elements."""
        self.parent = parent

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

    def extract(self):
        """Destructively rips this element out of the tree."""
        if self.parent is not None:
            del self.parent.contents[self.parent.index(self)]

        self.parent = None

        if self.previous_sibling is not None:
            self.previous_sibling.next_sibling = self.next_sibling

        if self.next_sibling is not None:
            self.next_sibling.previous_sibling = self.previous_sibling

        self.previous_sibling = self.next_sibling = None

        return self

    def _extract(self, self_index):
        """
        This is a method which decreases runtime if the index of self in parent.contents is already known.
        For Tag's insert method but may have other uses.
        Extracts self from the tree.
        :param self_index: should be equal to self.parent.index(self)
        """
        del self.parent.contents[self_index]

        self.parent = None

        if self.previous_sibling is not None:
            self.previous_sibling.next_sibling = self.next_sibling

        if self.next_sibling is not None:
            self.next_sibling.previous_sibling = self.previous_sibling

        self.previous_sibling = self.next_sibling = None

        return self

    def wrap(self, wrapper):
        me = self.replace_with(wrapper)
        wrapper.append(me)
        return wrapper

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
        """
        Makes the given element the immediate successor of this one.

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
        parent.insert(index + 1, successor)

    # find methods (using name, attrs, and text) go here. They were deleted b/c they are unnecessary.
