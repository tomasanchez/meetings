"""
Test Schemas
"""
from app.domain.schemas import CamelCaseModel


class TestSchemas:
    """
    Test for schemas.
    """

    class FooSchema(CamelCaseModel):
        """
        A test schema
        """
        foo: str
        bar: str | None
        foo_bar: str | None = None

    def test_camel_case_model(self):
        """
        GIVEN a CamelCaseModel
        WHEN a dict is created from the model
        THEN check the dict is as expected
        """
        model = self.FooSchema(foo="bar", bar="baz", foo_bar="bar_baz")

        assert model.dict() == {"foo": "bar", "bar": "baz", "foo_bar": "bar_baz"}

    def test_camel_case_model_with_none(self):
        """
        GIVEN a CamelCaseModel with a None value
        WHEN a dict is created from the model
        THEN dict omits the None value
        """
        model = self.FooSchema(foo="bar")

        assert model.dict() == {"foo": "bar"}

    def test_camel_case_model_is_camel_case(self):
        """
        GIVEN a CamelCaseModel with a None value in a list
        WHEN a json is created from the model
        THEN it is in camelcase
        """
        model = self.FooSchema(foo="bar", foo_bar="bar_baz")

        assert model.json() == '{"foo": "bar", "fooBar": "bar_baz"}'

    def test_camel_case_model_with_none_is_camel_case(self):
        """
        GIVEN a CamelCaseModel with a None value in a list
        WHEN a json is created from the model
        THEN it omits the None values
        """
        model = self.FooSchema(foo="bar")

        assert model.json() == '{"foo": "bar"}'
