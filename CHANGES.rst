Changelog
=========

2.5 - Unreleased
----------------

- Update tox.ini for latest tox.
  [stefan]


2.4 - 2022-11-17
----------------

- Upgrade to rl 3.1.
  [stefan]

- Update filename completion for readline 8.2.
  [stefan]

- Hide do_EOF from completion and help.
  [stefan]

- Quote newline characters between double quotes.
  [stefan]

- Improve documentation and examples.
  [stefan]

- Replace deprecated ``python setup.py test`` in tox.ini.
  [stefan]

- Remove deprecated ``test_suite`` from setup.py.
  [stefan]

- Remove setuptools from ``install_requires``.
  [stefan]

- Add a pyproject.toml file.
  [stefan]

- Include tests in sdist but not in wheel.
  [stefan]


2.3 - 2019-03-20
----------------

- Clear lastcmd when EOF is hit to avoid an infinite loop. See Python
  `issue 13500`_.
  [stefan]

- Drop explicit GPL because the PSF license is GPL-compatible anyway.
  [stefan]

- Update filename completion with new hooks.
  [stefan]

- Stop hiding the quoting module in completions and make it available as
  *kmd.quoting*.
  [stefan]

- Stop using *rl.completer.reset* because it overrides ~/.inputrc.
  [stefan]

- Stop using 2to3.
  [stefan]

- Require rl >= 3.0.
  [stefan]

.. _`issue 13500`: https://bugs.python.org/issue13500

2.2 - 2012-05-10
----------------

- String and filename quoting was not respected when *Kmd.run*
  was called with arguments.
  [stefan]

- Switch to a happier looking Sphinx theme.
  [stefan]

- Require rl >= 2.2.
  [stefan]

2.1.2 - 2012-04-14
------------------

- Update documentation more.
  [stefan]

2.1.1 - 2012-03-29
------------------

- Update documentation.
  [stefan]

2.1 - 2011-11-05
----------------

- Add *Kmd.input* method as extension point for subclasses.
  [stefan]

- Make sure hostname completion survives a missing hosts file.
  [stefan]

- Require rl >= 2.0.1.
  [stefan]

2.0 - 2011-10-06
----------------

- Add *Kmd.aliases* dictionary to define command aliases.
  [stefan]

- Refactor *Kmd.do_help* for easier customization.
  [stefan]

- Make sure error messages go to stderr.
  [stefan]

- Switch to pretty Sphinx-based docs.
  [stefan]

- Require rl >= 2.0.
  [stefan]

1.0 - 2011-07-14
----------------

- Initial release.
