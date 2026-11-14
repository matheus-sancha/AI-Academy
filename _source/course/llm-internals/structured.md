## TL;DR

A structured output is a reply the platform holds to a JSON Schema you supply. The older JSON mode guaranteed valid
JSON and could not guarantee the shape. A schema gives the shape: every field present, closed sets as enums, no
extra keys. It cannot give truth. A reply can match its schema exactly and still carry the wrong number. So the
schema fixes what downstream code can rely on, and the code still checks what the values say. This lesson covers
where the schema goes, the subset of JSON Schema the platform accepts, strict function tools, and the cases where
you get no parsed value at all.

## Why it matters

A flow, a database column or a function call all fail on a missing field and on a free-text value where a closed
set belongs. {{topic:temperature}} listed malformed JSON as a symptom and gave the fix as a schema plus validation.
{{topic:prompts}} showed one product's version of the same idea, a format locked when a prompt is saved. This lesson
is the API-level version, for code that calls a model directly.

## How it works

### Where the schema goes

Both APIs accept a schema. In Chat Completions it goes in `response_format`. In the Responses API it goes in
`text.format`, with `type`, `name`, `schema` and `strict` as sibling properties. The page recommends the feature for
function calling, for extracting structured data and for multi-step workflows. In Python, a Pydantic class can stand
in for the schema, and the SDK returns the parsed object.

<!-- volatile verified=2026-11 -->
*Adapted from the Responses API request on the structured outputs page, for a supplier material certificate:*

```json
{ "type": "json_schema", "name": "MaterialCertificate", "strict": true,
  "schema": {
    "type": "object",
    "properties": {
      "certificate_no": { "type": "string" },
      "heat_no": { "type": "string" },
      "grade": { "type": "string" },
      "yield_strength": { "type": ["number", "null"] },
      "yield_unit": { "type": ["string", "null"], "enum": ["MPa", "ksi"] }
    },
    "required": ["certificate_no", "heat_no", "grade", "yield_strength", "yield_unit"],
    "additionalProperties": false } }
```
<!-- /volatile -->

### The subset the platform accepts

<!-- volatile verified=2026-11 -->
Structured outputs support a subset of JSON Schema. The types are string, number, boolean, integer, object, array,
enum and `anyOf`, and the root object cannot be `anyOf`. Four rules shape every schema:

- **Every field is required.** To emulate an optional field, make its type a union with `null`, as the sample does.
- **Every object sets `additionalProperties` to false.**
- **A schema may have up to 100 object properties and five levels of nesting.**
- **Keys come back in the schema's order.** Reorder the schema to reorder the output.

Definitions and recursive schemas are supported. A list of keywords is not: `pattern`, `format`, `minLength` and
`maxLength` on strings, `minimum`, `maximum` and `multipleOf` on numbers, `minItems`, `maxItems` and `uniqueItems`
on arrays, and several object keywords such as `minProperties` and `patternProperties`.
<!-- /volatile -->

The unsupported list is the practical limit. Every rule that is a range or a pattern, such as a minimum yield
strength or a document-number format, has to live in your code.

<!-- unknown since=2026-11 -->
The page lists the unsupported keywords and does not say what happens when a schema uses one: whether the request
fails or the keyword is ignored. Test a schema on the deployment before you rely on any constraint in it.
<!-- /unknown -->

### Strict function tools

<!-- volatile verified=2026-11 -->
The same guarantee applies to a function's arguments when the function is declared with `strict: true`. The page
says structured outputs are not supported with parallel function calls, so set `parallel_tool_calls` to `false`.
That gives up the saving {{topic:functioncalling}} describes. The all-required rule applies to function
parameters too.
<!-- /volatile -->

### When there is no parsed value

<!-- volatile verified=2026-11 -->
The page's own JavaScript samples do not trust the result. They throw on a `refusal` before reading the parsed
object, and on the Responses API they check that the response status is `completed`, and throw on an error or on
incomplete details. So a schema-bound reply can still be a refusal or an incomplete response. The page also lists what the feature does not cover: bring-your-own-data scenarios,
Assistants or Foundry Agents Service, and the `gpt-audio` models. Support depends on the model and version, and
on API version `2024-08-01-preview` or later, including the GA `v1`.
<!-- /volatile -->

The second curated page, the Copilot Studio prompts overview, describes prompts as reusable instructions that
agents, workflows or apps can call, on the standard harness. It says nothing about JSON or schemas.

<!-- unknown since=2026-11 -->
The roadmap named JSON output in Copilot Studio as this topic's second source. The curated page does not cover it,
so that label was wrong. The Intermediate lesson {{topic:prompts}} covers the format its own sources document.
<!-- /unknown -->

## In practice at Technik

The capstone uses none of this. Its tools return text, its answers are prose, and its checks read that prose
({{topic:stageevals}}). The place Technik needs a schema is the supplier material certificate: ten sample PDFs,
one per heat of bar, each giving a certificate number, heat number, grade, strengths, elongation and hardness, with
one supplier reporting strength in ksi. Technik's purchase specification sets a minimum yield strength of 485 MPa.
{{module:automation-advanced}} covers a pipeline that reads them, and the schema above would be its extraction step.

It does three jobs. It forces a field for every value, with `null` where a certificate shows none. It closes the
unit to `MPa` or `ksi`, so a stray `psi` cannot arrive. And it makes the reply parseable without a regular
expression. It cannot do the fourth: the page's supported subset has no `minimum`, and a threshold is a business
rule anyway. A reading of `72` with the unit `MPa` fits the schema perfectly, and if that certificate printed
72 ksi it is wrong by a factor of nearly seven. So the code converts ksi to MPa, compares with 485 and routes the
certificate to a person on any doubt, because a valid reply is not a checked one ({{topic:docpipelines}}).

The capstone's argument types use `pattern` ({{topic:functioncalling}}). A strict version of those tools could not
carry it, so the format check would move from the type into the server's code.

<!-- unknown since=2026-11 -->
Nothing in the page says whether an agent hosted in Foundry can set `text.format` on its own model calls. The
page excludes Foundry Agents Service, and the capstone's hosted agent is the open case.
<!-- /unknown -->

## Design guidance

- **Use a schema when code reads the reply**, and prose when a person does.
- **Make every field required**, with an explicit `null` where a value may be absent.
- **Close every finite set with an enum**: units, operations, priorities.
- **Keep ranges, patterns and cross-field rules in code**, because the schema cannot hold them.
- **Check for a refusal and an incomplete status** before reading the parsed value.
- **Set `parallel_tool_calls` to `false`** for strict tools, and count the extra round trips.
- **Version the schema with the prompt**, and re-run the evaluation set when either changes ({{topic:evalstrategy}}).

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A constraint in the schema has no effect, or the request fails | The keyword is unsupported, and the page does not say which happens | Remove it, and validate in code |
| A field you meant to be optional is missing from the schema's `required` | Every field must be required | Use a union with `null` |
| A reply fits the schema and is wrong | A schema checks shape, never truth | Check values in code, and route doubt to a person |
| The parsed value is empty | A refusal, or a response that stopped early | Check the refusal and the status before parsing |
| Parallel tool calls vanish | Strict mode does not support them | Set `parallel_tool_calls` to `false` |
| The feature works on one deployment and not another | Support depends on model, version and API version | Check the supported list for your deployment |

## Key terms

**Structured output**: a reply held to a JSON Schema supplied with the request.

**JSON mode**: the older setting that guarantees valid JSON and does not guarantee a schema.

**Strict**: the flag that holds a function's arguments, or a response format, to its schema exactly.

**Nullable union**: a field type combined with `null`, used to emulate an optional field.
