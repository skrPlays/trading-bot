#Testing FWKs. Refer https://realpython.com/python-testing/
1. unitetst
2. nose2
3. pytest -> preferably this

#Assertion Methods
.assertEqual(a, b)	        .assertTrue(x)          .assertFalse(x)	                .assertIs(a, b)	
.assertIsNone(x)            .assertIn(a, b)         .assertIsInstance(a, b)         .assertIsNotInstance(a,b)

#Side Effects -> To resolve:-
1. Refactoring code to follow the Single Responsibility Principle
2. Mocking out any method or function calls to remove side effects
3. Using integration testing instead of unit testing for this piece of the application

#Executing Test Runners

#Testing Methodology
1. Create your inputs aka Fixtures
2. Execute the code, capturing the output
3. Compare the output with an expected result
4. Ensure 100% code coverage

#Handling Expected Failures
Use .assertRaises() as a context-manager

    def test_bad_type(self):
        data = "banana"
        with self.assertRaises(TypeError):           #Replace TypeError with any exception type you choose
            result = sum(data)

#Isolating Behaviors in Your Application

#Mocking REST calls, external module call, API calls etc.
https://github.com/getsentry/responses/tree/master/responses

    mocker.patch.object(outside_module, 'do_something')
    mocker.do_something.return_value(1)

For successive invocations of the same function but different outputs, use .side_effect()

    mocker.do_something.side_effect([1, 2])

#Testing in Multiple Environments -> Use Tox
$pip install tox
Configure in tox.ini
        
        [tox]
        envlist = py27, py36
        
        [testenv]
        deps = django                  #If you don’t create a setup.py, and your application has some dependencies from PyPI, you’ll need to specify those on a number of lines under the [testenv] section.
        
        skipsdist=True
        
        commands =
            python -m unittest discover

#Automating the Execution of Your Tests
Login to "https://travis-ci.com/" and authenticate with your GitHub credentials. Then create a file called .travis.yml with the following contents:

    language: python
    python:
      - "2.7"                               #Test against Python 2.7 and 3.7 (You can replace those versions with any you choose.)
      - "3.7"
    install:
      - pip install -r requirements.txt     #Install all the packages you list in requirements.txt (You should remove this section if you don’t have any dependencies.)
    script:
      - python -m unittest discover         #Run python -m unittest discover to run the tests
    matrix:
      include:
        - python: "2.7"
          script: "flake8"                  #Add the flake8 dependency to your requirements.txt file

#Passive Linting With flake8 -> http://flake8.pycqa.org/en/latest/user/options.html
    $ pip install flake8
    $ flake8 test.py
    test.py:6:1: E302 expected 2 blank lines, found 1
    test.py:23:1: E305 expected 2 blank lines after class or function definition, found 1
    test.py:24:20: W292 no newline at end of file

#Aggressive Linting With a Code Formatter
    $ pip install black
    $ black xyz.py          #Changes your code automatically to meet a collection of style and layout practices

#Testing for Performance Degradation Between Changes
1.timeit module

    def test():
        # ... your code
    
    if __name__ == '__main__':
        import timeit
        print(timeit.timeit("test()", setup="from __main__ import test", number=100))
    
2.pytest-benchmark plugin from pytest package
    
    $ def test_my_function(benchmark):
        result = benchmark(test)
    
#Testing for Security Flaws in Your Application
    $ pip install bandit

