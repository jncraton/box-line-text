Data Format
===========

This document describes the serialization and storage format for documents.

Specifications
--------------

- Must properly handle documents up 4k (3840px) in either portrait or landscape orientation. Specifically, documents up to 3840px by 3840px must be serialized correctly.
- Must allow up to 4k characters per text element
- Full Unicode text support

Considerations
--------------

- URL Encoding - This format primarily targets storage within the URL fragment (hash), so it tries to make efficient use of URL-safe characters.
- Size efficiency - This formats aims to be as compact as possible to maximize the amount of data that can be stored in the URL and provide URLs that are as short as possible.
- Speed - The URL can be updated on each keypress, so the process of serializing the document must be very fast.
- URL transparency - URL should be as readable as possible as plain text. Ideally, text from the document should be present and readable in the URL to provide context for what we might be linking to.

### Positions

Elements are aligned to a 64px grid, so we need to be able to store 3840px / 64px = 60 distinct position values. This works out nicely for efficent position storage in single character base64 encoded values.

### Text values

We need to ensure that these are properly encoded to be safe in a URL. We will simply use URL encoding on the text value for space efficiency and maximum URL readability.

Format
------

- Format version (1 byte)
- List of elements

### Element

- Left (6 bits, 1 b64 byte)
- Top (6 bits, 1 b64 byte)
- Width (6 bits, 1 b64 byte)
- Height (6 bits, 1 b64 byte)
- Text content

Example Encoding
----------------

Let's take a look at a simple "Hello World" document. It contains a box with the word "Hello", a box with the word "World", and a floating smiling face emoji. It is encoded as:

    1BBCBHello;EBCBWorld;DCAAAC😀;

Let's break that down:

- 1 - Format version 1
- Start of element
    - B - Left is position 1
    - B - Top is position 1
    - C - Width is 2
    - B - Height is 1
    - Hello - Text content
- ; - Start of next element
    - E - Left is position 4
    - B - Top is position 1
    - C - Width is 2
    - B - Height is 1
    - AF - There are 5 text characters
    - World - Text content
- ; - Start of next element
    - D - Left is position 3
    - C - Top is position 2
    - A - Width is 0
    - A - Height is 0
    - 😀 - Text content

Alternatives 
============

We have several fragment-safe characters that we haven't made use of. Here's the full set:

    ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890?/:@-._~!$&'()*+,;=

We could use those to pack in extra information.

In place of a single element separator, we could use record separators such as the following to save space.

    : V line
    ; V line with text
    _ H line
    ~ H line with text
    & Box
    @ Box with text
    = Text
