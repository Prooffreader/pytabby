Order of tests:


1. test_validators::test_fn__determine_schema_type
2. test_validators::test_fn__validate_schema because it depends on test_fn__determine_schema_type, and breaking tests depend on valid schema
   test_validators non-breaking unit tests
3. test_validators breaking unit tests
4. (integration) test_validators::validate_all
5.
6.
7.
8.
9.


-4:
-3:
-2:
-1: