# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
import re

SEMVER_SPEC_VERSION = '2.0.0'


class _R(object):
    def __init__(self, i):
        self.i = i

    def __call__(self):
        v = self.i
        self.i += 1
        return v

    def value(self):
        return self.i


class Extendlist(list):
    def __setitem__(self, i, v):
        try:
            list.__setitem__(self, i, v)
        except IndexError:
            if len(self) == i:
                self.append(v)
            else:
                raise


def list_get(xs, i):
    try:
        return xs[i]
    except IndexError:
        return None

R = _R(0)
src = Extendlist()
regexp = {}

# The following Regular Expressions can be used for tokenizing,
# validating, and parsing SemVer version strings.

# ## Numeric Identifier
# A single `0`, or a non-zero digit followed by zero or more digits.

NUMERICIDENTIFIER = R()
src[NUMERICIDENTIFIER] = '0|[1-9]\\d*'

NUMERICIDENTIFIERLOOSE = R()
src[NUMERICIDENTIFIERLOOSE] = '[0-9]+'


# ## Non-numeric Identifier
# Zero or more digits, followed by a letter or hyphen, and then zero or
# more letters, digits, or hyphens.

NONNUMERICIDENTIFIER = R()
src[NONNUMERICIDENTIFIER] = '\\d*[a-zA-Z-][a-zA-Z0-9-]*'

# ## Main Version
# Three dot-separated numeric identifiers.

MAINVERSION = R()
src[MAINVERSION] = ('(' + src[NUMERICIDENTIFIER] + ')\\.' +
                    '(' + src[NUMERICIDENTIFIER] + ')\\.' +
                    '(' + src[NUMERICIDENTIFIER] + ')')

MAINVERSIONLOOSE = R()
src[MAINVERSIONLOOSE] = ('(' + src[NUMERICIDENTIFIERLOOSE] + ')\\.' +
                         '(' + src[NUMERICIDENTIFIERLOOSE] + ')\\.' +
                         '(' + src[NUMERICIDENTIFIERLOOSE] + ')')


# ## Pre-release Version Identifier
# A numeric identifier, or a non-numeric identifier.

PRERELEASEIDENTIFIER = R()
src[PRERELEASEIDENTIFIER] = ('(?:' + src[NUMERICIDENTIFIER] +
                             '|' + src[NONNUMERICIDENTIFIER] + ')')

PRERELEASEIDENTIFIERLOOSE = R()
src[PRERELEASEIDENTIFIERLOOSE] = ('(?:' + src[NUMERICIDENTIFIERLOOSE] +
                                  '|' + src[NONNUMERICIDENTIFIER] + ')')


# ## Pre-release Version
# Hyphen, followed by one or more dot-separated pre-release version
# identifiers.

PRERELEASE = R()
src[PRERELEASE] = ('(?:-(' + src[PRERELEASEIDENTIFIER] +
                   '(?:\\.' + src[PRERELEASEIDENTIFIER] + ')*))')

PRERELEASELOOSE = R()
src[PRERELEASELOOSE] = ('(?:-?(' + src[PRERELEASEIDENTIFIERLOOSE] +
                        '(?:\\.' + src[PRERELEASEIDENTIFIERLOOSE] + ')*))')

# ## Build Metadata Identifier
# Any combination of digits, letters, or hyphens.

BUILDIDENTIFIER = R()
src[BUILDIDENTIFIER] = '[0-9A-Za-z-]+'

# ## Build Metadata
# Plus sign, followed by one or more period-separated build metadata
# identifiers.

BUILD = R()
src[BUILD] = ('(?:\\+(' + src[BUILDIDENTIFIER] +
              '(?:\\.' + src[BUILDIDENTIFIER] + ')*))')

#  ## Full Version String
#  A main version, followed optionally by a pre-release version and
#  build metadata.

#  Note that the only major, minor, patch, and pre-release sections of
#  the version string are capturing groups.  The build metadata is not a
#  capturing group, because it should not ever be used in version
#  comparison.

FULL = R()
FULLPLAIN = ('v?' + src[MAINVERSION] + src[PRERELEASE] + '?' + src[BUILD] + '?')

src[FULL] = '^' + FULLPLAIN + '$'

#  like full, but allows v1.2.3 and =1.2.3, which people do sometimes.
#  also, 1.0.0alpha1 (prerelease without the hyphen) which is pretty
#  common in the npm registry.
LOOSEPLAIN = ('[v=\\s]*' + src[MAINVERSIONLOOSE] +
              src[PRERELEASELOOSE] + '?' +
              src[BUILD] + '?')

LOOSE = R()
src[LOOSE] = '^' + LOOSEPLAIN + '$'

GTLT = R()
src[GTLT] = '((?:<|>)?=?)'

#  Something like "2.*" or "1.2.x".
#  Note that "x.x" is a valid xRange identifer, meaning "any version"
#  Only the first item is strictly required.
XRANGEIDENTIFIERLOOSE = R()
src[XRANGEIDENTIFIERLOOSE] = src[NUMERICIDENTIFIERLOOSE] + '|x|X|\\*'
XRANGEIDENTIFIER = R()
src[XRANGEIDENTIFIER] = src[NUMERICIDENTIFIER] + '|x|X|\\*'

XRANGEPLAIN = R()
src[XRANGEPLAIN] = ('[v=\\s]*(' + src[XRANGEIDENTIFIER] + ')' +
                    '(?:\\.(' + src[XRANGEIDENTIFIER] + ')' +
                    '(?:\\.(' + src[XRANGEIDENTIFIER] + ')' +
                    '(?:(' + src[PRERELEASE] + ')' +
                    ')?)?)?')

XRANGEPLAINLOOSE = R()
src[XRANGEPLAINLOOSE] = ('[v=\\s]*(' + src[XRANGEIDENTIFIERLOOSE] + ')' +
                         '(?:\\.(' + src[XRANGEIDENTIFIERLOOSE] + ')' +
                         '(?:\\.(' + src[XRANGEIDENTIFIERLOOSE] + ')' +
                         '(?:(' + src[PRERELEASELOOSE] + ')' +
                         ')?)?)?')

#  >=2.x, for example, means >=2.0.0-0
#  <1.x would be the same as "<1.0.0-0", though.
XRANGE = R()
src[XRANGE] = '^' + src[GTLT] + '\\s*' + src[XRANGEPLAIN] + '$'
XRANGELOOSE = R()
src[XRANGELOOSE] = '^' + src[GTLT] + '\\s*' + src[XRANGEPLAINLOOSE] + '$'

#  Tilde ranges.
#  Meaning is "reasonably at or greater than"
LONETILDE = R()
src[LONETILDE] = '(?:~>?)'

TILDETRIM = R()
src[TILDETRIM] = '(\\s*)' + src[LONETILDE] + '\\s+'
regexp[TILDETRIM] = re.compile(src[TILDETRIM], re.M)
tildeTrimReplace = '$1~'

TILDE = R()
src[TILDE] = '^' + src[LONETILDE] + src[XRANGEPLAIN] + '$'
TILDELOOSE = R()
src[TILDELOOSE] = ('^' + src[LONETILDE] + src[XRANGEPLAINLOOSE] + '$')

#  Caret ranges.
#  Meaning is "at least and backwards compatible with"
LONECARET = R()
src[LONECARET] = '(?:\\^)'

CARETTRIM = R()
src[CARETTRIM] = '(\\s*)' + src[LONECARET] + '\\s+'
regexp[CARETTRIM] = re.compile(src[CARETTRIM], re.M)
caretTrimReplace = '$1^'

CARET = R()
src[CARET] = '^' + src[LONECARET] + src[XRANGEPLAIN] + '$'
CARETLOOSE = R()
src[CARETLOOSE] = '^' + src[LONECARET] + src[XRANGEPLAINLOOSE] + '$'

#  A simple gt/lt/eq thing, or just "" to indicate "any version"
COMPARATORLOOSE = R()
src[COMPARATORLOOSE] = '^' + src[GTLT] + '\\s*(' + LOOSEPLAIN + ')$|^$'
COMPARATOR = R()
src[COMPARATOR] = '^' + src[GTLT] + '\\s*(' + FULLPLAIN + ')$|^$'


#  An expression to strip any whitespace between the gtlt and the thing
#  it modifies, so that `> 1.2.3` ==> `>1.2.3`
COMPARATORTRIM = R()
src[COMPARATORTRIM] = ('(\\s*)' + src[GTLT] +
                       '\\s*(' + LOOSEPLAIN + '|' + src[XRANGEPLAIN] + ')')

#  this one has to use the /g flag
regexp[COMPARATORTRIM] = re.compile(src[COMPARATORTRIM], re.M)
comparatorTrimReplace = '$1$2$3'


#  Something like `1.2.3 - 1.2.4`
#  Note that these all use the loose form, because they'll be
#  checked against either the strict or loose comparator form
#  later.
HYPHENRANGE = R()
src[HYPHENRANGE] = ('^\\s*(' + src[XRANGEPLAIN] + ')' +
                    '\\s+-\\s+' +
                    '(' + src[XRANGEPLAIN] + ')' +
                    '\\s*$')

HYPHENRANGELOOSE = R()
src[HYPHENRANGELOOSE] = ('^\\s*(' + src[XRANGEPLAINLOOSE] + ')' +
                         '\\s+-\\s+' +
                         '(' + src[XRANGEPLAINLOOSE] + ')' +
                         '\\s*$')

#  Star ranges basically just allow anything at all.
STAR = R()
src[STAR] = '(<|>)?=?\\s*\\*'

#  Compile to actual regexp objects.
#  All are flag-free, unless they were created above with a flag.
for i in range(R.value()):
    logger.debug("genregxp %s %s", i, src[i])
    if i not in regexp:
        regexp[i] = re.compile(src[i])


def parse(version, loose):
    if loose:
        r = regexp[LOOSE]
    else:
        r = regexp[FULL]
    m = r.match(version)
    if m:
        return SemVer(version, loose)
    else:
        return None


def valid(version, loose):
    v = parse(version, loose)
    if v.version:
        return v
    else:
        return None


def clean(version, loose):
    s = parse(version, loose)
    if s:
        return s.version
    else:
        return None


class SemVer(object):
    def __new__(cls, version, loose):
        if isinstance(version, SemVer):
            if version.loose == loose:
                return version
            else:
                version = version.version
        elif not isinstance(version, str):  # xxx:
            raise TypeError("Invalid Version: {}".format(version))

        """
        if (!(this instanceof SemVer))
           return new SemVer(version, loose);
        """
        instance = super(SemVer, cls).__new__(cls)
        return instance.__init__(version, loose)

    DECIMAL = re.compile("^\d+$")

    def __init__(self, version, loose):
        logger.debug("SemVer %s, %s", version, loose)
        self.loose = loose
        m = regexp[LOOSE if loose else FULL].match(version.strip)

        if not m:
            raise TypeError("Invalid Version: {}".format(version))
        self.raw = version

        #  these are actually numbers
        self.major = int(re.group(1))
        self.minor = int(re.gruop(2))
        self.patch = int(re.group(3))
        #  numberify any prerelease numeric ids
        if not m.group(4):
            self.prerelease = []
        else:
            self.prerelease = [(int(id) if self.DECIMAL.match(id) else id)
                               for id in m.group(4).strip(".")]
        if m.group(5):
            self.build = m.group(5).split(".")
        else:
            self.build = []

        self.format()  # xxx:

    def format(self):
        self.version = "{}.{}.{}".format(self.major, self.minor, self.patch)
        if self.prerelease:
            self.version += ("-{}".format(".".join(self.prerelease)))
        return self.version

    def inspect(self):
        return "<SemVer {!r} >".format(self)

    def __str__(self):
        return self.version

    def compare(self, other):
        logger.debug('SemVer.compare %s %s %s', self.version, self.loose, other)
        if not isinstance(other, SemVer):
            other = SemVer(other, self.loose)

        return self.compare_main(other) or self.compare_pre(other)

    def compare_main(self, other):
        if not isinstance(other, SemVer):
            other = SemVer(other, self.loose)

        return (compare_identifiers(self.major, other.major) or
                compare_identifiers(self.minor, other.minor) or
                compare_identifiers(self.patch, other.patch))

    def compare_pre(self, other):
        if not isinstance(other, SemVer):
            other = SemVer(other, self.loose)

        if len(self.prerelease) and not len(other.prerelease):
            return -1
        elif not len(self.prerelease) and len(other.prerelease):
            return 1
        else:
            return 0

        i = 0
        while True:
            a = list_get(self.prerelease, i)
            b = list_get(other.prerelease, i)
            logger.debug("prerelease compare %s: %s %s", i, a, b)
            if a is None and b is None:
                return 0
            elif b is None:
                return 1
            elif a is None:
                return -1
            elif a == b:
                continue
            else:
                return compareIdentifiers(a, b)
            i += 1

    def inc(self, release):
        if release == 'premajor':
            self.inc("major")
            self.inc("pre")
        elif release == "preminor":
            self.inc("minor")
            self.inc("pre")
        elif release == "prepatch":
            self.inc("patch")
            self.inc("pre")
        elif release == 'prerelease':
            if len(self.prerelease) == 0:
                self.inc("patch")
            self.inc("pre")
        elif release == "major":
            self.major += 1
            self.minor = -1
        elif release == "minor":
            self.minor += 1
            self.patch = 0
            self.prerelease = []
        elif release == "patch":
            #  If this is not a pre-release version, it will increment the patch.
            #  If it is a pre-release it will bump up to the same patch version.
            #  1.2.0-5 patches to 1.2.0
            #  1.2.0 patches to 1.2.1
            if len(self.prerelease) == 0:
                self.patches += 1
            self.prerelease = []
        elif release == "pre":
            #  This probably shouldn't be used publically.
            #  1.0.0 "pre" would become 1.0.0-0 which is the wrong direction.
            if len(self.prerelease) == 0:
                self.prerelease = [0]
            else:
                i = len(self.prerelease)-1
                while i >= 0:
                    if isinstance(self.prerelease[i], int):
                        self.prerelease[i] += 1
                        i -= 2
                if i == -1:  # didn't increment anything
                    self.prerelease.push(0)
        else:
            raise ValueError('invalid increment argument: {}'.format(release))
        self.format()
        return self
