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

- Text length (12 bits, 2 b64 bytes) 
- Left (6 bits, 1 b64 byte)
- Top (6 bits, 1 b64 byte)
- Width (6 bits, 1 b64 byte)
- Height (6 bits, 1 b64 byte)
- Text content ({text.length} bytes plus any URL encoding overhead)

Example Encoding
----------------

Let's take a look at a simple "Hello World" document. It contains a box with the word "Hello", a box with the word "World", and a floating smiling face emoji. It is encoded as:

    1BBCBAFHelloEBCBAFWorldDCAAAC😀

Let's break that down:

- 1 - Format version 1
- Start of element
    - B - Left is position 1
    - B - Top is position 1
    - C - Width is 2
    - B - Height is 1
    - AF - There are 5 text characters
    - Hello - The expected 5 characters
- Start of element
    - E - Left is position 4
    - B - Top is position 1
    - C - Width is 2
    - B - Height is 1
    - AF - There are 5 text characters
    - World - The expected 5 characters
- Start of element
    - D - Left is position 3
    - C - Top is position 2
    - A - Width is 0
    - A - Height is 0
    - AC - There are 2 text characters
    - 😀 - The expected 2 characters

Header Run Length Encoding
--------------------------

We have at least a couple ("~" and ".") URL-safe characters not used for our base64 encoding so we can use those to pack in extra information. Let's consider a few scenarios:

- Floating text elements don't need their width and height, so they waste two bytes
- Elements with no text waste two bytes encoding their text length

We could use a more complex scheme to identify these types of element, or we could pack the redundant data more efficiently. The redundancy comes in the form of repeated 0 values ('A' in base64), so we use our two spare characters to implement run length encoding.

Specifically, a '~' in a header represents two zero values, and a '.' in a header represents three zero values. This mean the the following elements now take less than 6 bytes for their headers:

- Less than 64 bytes of floating text uses a 4 byte header
- A horizontal line requires 4 bytes total
- A vertical line requires 5 bytes total
- An empty box requires 5 bytes total
