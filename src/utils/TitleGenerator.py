class TitleGenerator:
    @staticmethod
    def generateTitle(modes:str):
        """
        Generate a title string based on the provided modes.

        Args:
            modes (str): A string containing mode characters where:
                            - 't' represents "Tangent" mode
                            - 'a' represents "Adjoint" mode

        Returns:
            str: A title string with mode names joined by " over ".
                    Example: "Tangent over Adjoint over Tangent"
        """
        content:list[str] = []

        for char in modes:
            if char == 't':
                content.append("Tangent")
            elif char == 'a':
                content.append("Adjoint")

        title:str = " over ".join(content)

        return title