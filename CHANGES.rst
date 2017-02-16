Changelog
=========

2.3 - Unreleased
----------------

- Stop using *rl.completer.reset* because it overrides ~/.inputrc.
  [stefan]

- Require rl >= 2.5.
  [stefan]


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