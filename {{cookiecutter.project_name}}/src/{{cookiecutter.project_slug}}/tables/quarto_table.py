from typing import Any


class InvalidDataFrameError(TypeError):
    def __init__(self):
        super().__init__("The input must be a pandas DataFrame.")


class QuartoDisplayTable:
    """
    A wrapper class for a pandas DataFrame to enable proper display in both LaTeX and HTML documents.

    This class provides methods to render the DataFrame as LaTeX or HTML, which can be useful for
    generating reports or documents in Quarto.

    Note: pandas is an optional dependency and must be installed separately. If pandas is not installed,
    an ImportError will be raised when attempting to use this class.
    """

    def __init__(self, df: Any):
        """
        Initialize the QuartoDisplayTable with a pandas DataFrame.

        Args:
            df (Any): The DataFrame to wrap. This should be a pandas DataFrame.

        Raises:
            ImportError: If pandas is not installed.
        """
        try:
            import pandas as pd  # ty: ignore[unresolved-import]
        except ImportError as e:
            e.msg = "pandas is required to use QuartoDisplayTable."
            raise

        if not isinstance(df, pd.DataFrame):
            raise InvalidDataFrameError()

        self.df = df

    def _repr_latex_(self) -> str:
        """
        Generate a LaTeX representation of the DataFrame.

        Returns:
            str: The LaTeX string representation of the DataFrame.
        """
        return self.df.to_latex(index=False, caption=None, escape=True)

    def _repr_html_(self) -> str:
        """
        Generate an HTML representation of the DataFrame.

        Returns:
            str: The HTML string representation of the DataFrame.
        """
        return self.df.to_html(index=False)
