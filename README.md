OARepo documents
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
-----
This library contains data model for creating documents. 
This data model is not usable by it self, you have to add it to your own data model as it is shown in "Using data model".
New document can by also created by provided DOI, as it is shown in "Document from DOI"

Using data model
----------------
Document json schema, es mapping and marshmallow is taken from ```invenio-app-ils/documents``` with some properties changed to data type ```multilingual string``` from oarepo-multilingual library.
All properties that are changed to multilingual are listed in "Changes"
### Changes
- abstract
- alternative_abstracts
- alternative_titles
- conference_info (only property "title")
- license (only property "title")
- note
- publication_info (only property "journal_title")
- title
- urls (only property "description")

### Json Schema
Add documents json schema to your schema with keyword ```allOf``` and ```"$ref": "/schemas/document-v1.0.0.json#/definitions/Document"```
#### Example
```json
{
  "type": "object",
  "allOf": [
    {
      "properties": {
        "extra_property": {
          "type": "string"
        }
      }
    },
    {
      "$ref": "/schemas/document-v1.0.0.json#/definitions/Document"
    }
  ],
  "additionalProperties": "false"
}
```
### Mapping
Add documents mapping to your elastic search mapping with ```"oarepo:extends": "document-v1.0.0.json#/Document"``` from library "oarepo-extends""
#### Example
```json
{
  "mappings": {
    "dynamic": "strict",
    "oarepo:extends": "document-v1.0.0.json#/Document",
    "properties": {
         "extra_property": {
        "type": "text"
      }
    }
  }
}
```
### Marshmallow
Inherit your class from ```DocumentSchemaV1```
#### Example

```python
from oarepo_sitemaps.marshmallow.document import DocumentSchemaV1


class SampleSchemaV1(DocumentSchemaV1):
 extra_property = fields.String(validate=validate.Length(min=5), required=False) 
```
Document from DOI
-----------------
You can create new document record from existing DOI with url in format 'server/record_class/document/doi'.
This request will return existing document record, if document with that DOI already exists in your database.
If there is no document with this DOI in database, it will be created a new one via CrossRef client and metadata from this new document will be returned.
This new document will have its DOI as metadata in property "alternative_identifiers" with scheme "DOI".
### Examples
```python
 url = "https://localhost:5000/records/document/10.5281/zenodo.3883620"
```


 [image]: https://img.shields.io/travis/oarepo/oarepo-documents.svg
  [1]: https://travis-ci.com/github/oarepo/oarepo-documents
  [2]: https://img.shields.io/coveralls/oarepo/oarepo-documents.svg
  [3]: https://coveralls.io/r/oarepo/oarepo-documents
  [4]: https://img.shields.io/github/license/oarepo/oarepo-documents.svg
  [5]: https://github.com/oarepo/oarepo-documents/blob/master/LICENSE
  [6]: https://img.shields.io/pypi/v/oarepo-documents.svg
  [7]: https://pypi.org/pypi/oarepo-documents