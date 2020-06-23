Data Format
===========

This document describes the serialization and storage format for documents.

Specifications
--------------

- Must properly handle documents up 4k (3840px) in either portrait or landscape orientation. Specifically, documents up to 3840px by 3840px must be serialized correctly.
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

- Global header terminated by semicolon
    - This is currently unused, but could be used for future features such as global options and styles.
- List of elements separated by semicolons
- Example: `header;element;element;element`

### Element

- Byte 0 - Element header
    - 1 Bit - hasWidth
    - 1 Bit - hasHeight
    - 1 Quaternary Digit - Decoration [None, 1, 2, 3] (
      - Box - 1=Color 1, 2=Color 2, 3=Color 3, 0=No color
      - Line - 1=lower arrow, 2=upper arrow, 3=both, 0=No arrows
      - Text - 1=Double size, 0=Plain
    - 1 Quinary Digit - Reserved for later use
- Byte 1 - Left position
    - 1 base60 positive integer
- Byte 2 - Top position
    - 1 base 60 positive integer
- Byte 3 - Element width if required by header
    - 1 base 60 positive integer
- Byte 4 - Element height if requred by header
    - 1 base 60 positive integer
- Bytes 5+ - Text content

- Left (6 bits, 1 b64 byte)
- Top (6 bits, 1 b64 byte)
- Width (6 bits, 1 b64 byte)
- Height (6 bits, 1 b64 byte)
- Text content

Example Encoding
----------------

Let's take a look at a simple "Hello World" document. It contains a box with the word "Hello", a box with the word "World", and a large floating smiling face emoji. It is encoded as:

    ;c1121Hello;f4121World;212😀

Let's break that down:

- Empty global header
- ; - Start of element
    - c - Element with width, height, and decoration 0
    - 1 - Left is position 1
    - 1 - Top is position 1
    - 2 - Width is 2
    - 1 - Height is 1
    - Hello - Text content
- ; - Start of element
    - f - Element with width, height, and decoration 1
    - 4 - Left is position 4
    - 1 - Top is position 1
    - 2 - Width is 2
    - 1 - Height is 1
    - World - Text content
- ; - Start of element
    - 2 - Element with no width, no height, and decoration 3
    - 1 - Left is position 1
    - 2 - Top is position 2
    - 😀 - Text content

Here is the full URL for this sample document:

https://develop--box-line-text.netlify.app/#;c1121Hello;f4121World;212😀


Notes
=====

Here's the full set of fragment-safe characters:

    ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890?/:@-._~!$&'()*+,;=
We use these in the following order for up to base 80 encoding:

```0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_?/:@.~!$&'()*+,=```

The semicolon is reserved for use as a record separator.