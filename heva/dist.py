class _Distribution:
    """
    Abstract base class representing a distribution
    """

    def loc(self):
        raise NotImplementedError("Must be implemented by subclass")

    def scale(self):
        raise NotImplementedError("Must be implemented by subclass")

    def shape(self):
        raise NotImplementedError("Must be implemented by subclass")

    def pdf(self):
        raise NotImplementedError("Must be implemented by subclass")

    def cdf(self):
        raise NotImplementedError("Must be implemented by subclass")

    def logpdf(self):
        raise NotImplementedError("Must be implemented by subclass")
