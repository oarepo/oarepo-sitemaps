OARepo sitemaps
====================
[![image][]][1]
[![image][2]][3]
[![image][4]][5]
[![image][6]][7]

Instalation
----------
```bash
    pip install oarepo-sitemaps
```

Usage
----------
OARepo module that creates sitemap for a repository. Sitemap includes only records, that are in state "published" and can be viewed by public. 
Created sitemap is accessible on ```server/sitemap.xml``` url.

Configuration
-------------
Default number of record per one sitemap is 10000, this can be changed in configuration with ```'SITEMAP_MAX_URL_COUNT``` set to a different number.

Example
-------
```xml
<?xml version="1.0" encoding="utf-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
 <url>
  <loc>http://localhost:5000/cesnet/records/1</loc>
  <lastmod>2021-05-24</lastmod>
  <changefreq>weakly</changefreq>
  <priority>1</priority>
 </url>
 <url>
  <loc>http://localhost:5000/cesnet/records/2</loc>
  <lastmod>2021-05-24</lastmod>
  <changefreq>weakly</changefreq>
  <priority>1</priority>
 </url>
</urlset>
```
 [image]: https://img.shields.io/travis/oarepo/oarepo-sitemaps.svg
  [1]: https://travis-ci.com/github/oarepo/oarepo-sitemaps
  [2]: https://img.shields.io/coveralls/oarepo/oarepo-sitemaps.svg
  [3]: https://coveralls.io/r/oarepo/oarepo-sitemaps
  [4]: https://img.shields.io/github/license/oarepo/oarepo-sitemaps.svg
  [5]: https://github.com/oarepo/oarepo-documents/blob/master/LICENSE
  [6]: https://img.shields.io/pypi/v/oarepo-sitemaps.svg
  [7]: https://pypi.org/pypi/oarepo-sitemaps