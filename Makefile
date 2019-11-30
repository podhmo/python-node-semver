test:
	python setup.py test

# DST=README.rst
# SED=$(shell which gsed 2>/dev/null || which sed)
# default:
# 	echo semver > ${DST}
# 	echo ================= >> ${DST}
# 	echo "" >> ${DST}
# 	echo "python version of [node-semver](https://github.com/isaacs/node-semver)" >> ${DST}
# 	echo "" >> ${DST}
# 	echo ".. code:: python\n" >> ${DST}
# 	cat ./examples/readme.py | $(SED) 's/^\(.\)/   \1/g' >> ${DST}
