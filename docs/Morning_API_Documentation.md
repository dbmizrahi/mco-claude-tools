[Skip to content](#main)

# Build on _morning_

REST endpoints for documents, clients, expenses, payments and more. JSON over HTTPS, authenticated with OAuth 2.0.

[Explore the API](https://developers.morning.co/api)

## Two ways to build on morning

[**REST API** Create documents, manage clients and expenses, take payments, and receive webhooks — with a sandbox for every step. `**POST** /documents` Open the API documentation](https://developers.morning.co/api) [**MCP Server Soon** Let Claude Code, Cursor or VS Code search your documents, clients and expenses in plain language, on your own API key. ![](https://developers.morning.co/logos/claude-code.svg)![](https://developers.morning.co/logos/cursor.svg)![](https://developers.morning.co/logos/vscode.svg) Preview the MCP Server](https://developers.morning.co/mcp)

-   Getting Started
-   Environments
-   Get started
    -   Authentication
        -   postObtain an Access Token
-   Resources
    -   Documents
        -   postAdd Document
        -   postSearch Documents
        -   postSearch Payments in Documents
        -   postGet a Preview Document
        -   getGet Document Information
        -   getGet Document Templates
        -   getGet Document Types
        -   getGet Document Statuses
        -   getGet Document
        -   getGet Linked Documents
        -   getGet Document Download Links
        -   postClose Document
        -   postOpen Document
    -   Items
        -   postAdd Item
        -   getGet Item
        -   putUpdate Item
        -   delDelete Item
        -   postSearch Items
    -   Clients
        -   postAdd Client
        -   getGet Client
        -   putUpdate Client
        -   delDelete Client
        -   postSearch Clients
        -   postAssociate Documents to a Client
        -   postUpdate Client Balance
        -   postMerge Clients
    -   Suppliers
        -   postAdd Supplier
        -   getGet Supplier
        -   putUpdate Supplier
        -   delDelete Supplier
        -   postSearch Suppliers
        -   postMerge Suppliers
    -   Expenses
        -   postAdd Expense
        -   postSearch Expenses
        -   getGet Expense
        -   putUpdate Expense
        -   delDelete Expense
        -   getGet Allowed Expenses Statuses
        -   postClose Expense
        -   postOpen Expense
        -   getUpload Expense File · Step 1: Get Upload URL
        -   postUpload Expense File · Step 2: Send the File
        -   postSearch Expense Drafts
    -   Payments
        -   postGet Payment Form
        -   postSearch Credit Card Tokens
        -   postCharge Credit Card Token
-   Integrations
    -   Partners
        -   getGet Connected Users
        -   postRequest User Approval
        -   delDisconnect Partner User
    -   Webhooks
        -   EventDocument Created
        -   EventClient Created
        -   EventSupplier Created
        -   EventPayment Received
        -   EventSale Page Contacted
        -   EventSale Page Order Paid
        -   EventExpense Draft Parsed
        -   EventExpense Draft Declined
        -   EventExpense File Updated
        -   EventFile Infected
-   Reference
    -   Reference
        -   getGet Supported Business Categories
        -   getGet Supported Countries
        -   getGet Supported Cities
        -   getGet Supported Currencies
    -   Errors

[![redocly logo](https://cdn.redoc.ly/redoc/logo-mini.svg)API docs by Redocly](https://redocly.com/redoc/)

# morning API Documentation (2.0.0)

## Getting Started

Welcome to the morning API.

### About morning

Morning is a business management platform that helps companies manage invoicing, accounting, payments, and their overall financial operations.

The Morning API provides programmatic access to the platform, enabling you to automate workflows and seamlessly integrate Morning's capabilities into your own applications.

The API is built around REST principles and uses standard HTTP methods and status codes. All API communication is conducted over HTTPS, and all request and response bodies are JSON-encoded.

Authentication is implemented using OAuth 2.0, providing secure, token-based authorization. Applications obtain access tokens that must be included in API requests to securely access Morning resources according to granted permissions.

## Environments

We provide two environments for API development:

**Production** - Live operations with real data.

**Sandbox** - Testing and development. No real data is affected.

Each environment requires its own set of API keys.

We recommend building and testing your integration in the sandbox environment before switching to production.

Base URLs:

https://api.greeninvoice.co.il/api/v1ProductionSandbox

## Authentication

Our APIs use the **OAuth 2.0 protocol** for authentication and authorization.

To get started:

1.  Obtain your API keys (OAuth 2.0 client credentials) for your relevant business as explained [here](https://support.greeninvoice.co.il/kb/he/article/%D7%90%D7%99%D7%9A-%D7%9C%D7%99%D7%A6%D7%95%D7%A8-%D7%9E%D7%A4%D7%AA%D7%97%D7%95%D7%AA-api) (Hebrew).
2.  Request an access token from our authentication server using the endpoint below.
3.  Include the returned `accessToken` as a `Bearer` token in the `Authorization` header of all subsequent API requests:

```
Authorization: Bearer <accessToken>
```

## Obtain an Access Token

post/idp/v1/oauth/token

posthttps://api.morning.co/idp/v1/oauth/tokenProductionSandbox

This endpoint returns an access token (issued as a signed JWT) in the response body as `accessToken`.

**NOTES:**

-   Please be advised that **the `accessToken` is valid for 1 hour.** Once a token becomes invalid, requests to protected endpoints will return a `401 Unauthorized` error, and you will need to request a new token.
-   The access token is scoped to the business associated with your API keys.

-   Error Handling - All error responses follow the OAuth 2.0 error format (RFC 6749):

| Status | Error                                                             | Description |
| :-- | :-- | :-- |
| 400 | `invalid_request` | Missing `grant_type` parameter |
| 400 | `unsupported_grant_type` | `grant_type` is not `client_credentials` |
| 400 | `invalid_grant` | API key privilege is expired, revoked, or pending |
| 400 | `unauthorized_client` | No active subscription, or subscription does not include API access |
| 401 | `invalid_client` | Missing or incorrect `client_id`/`client_secret`, or application/account is blocked |

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="grant_type"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">grant_type</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><span class="sc-Nxspf lmPA-Dn">Value:</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"client_credentials"</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>OAuth 2.0 grant type. Must be <code>client_credentials</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="client_id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">client_id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>API Key Client ID. For example: <code>a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d</code>.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="client_secret"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">client_secret</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>API Key Client Secret. Keep it server-side — never embed it in client-side code or commit it to source control. For example: <code>Ex4mpleS3cret-DoNotUse</code>.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Access token successfully generated

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="accessToken"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">accessToken</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The access token to use as <code>Authorization: Bearer &lt;token&gt;</code> header</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="tokenType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">tokenType</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><span class="sc-Nxspf lmPA-Dn">Value:</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"Bearer"</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The token type</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="expiresAt"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">expiresAt</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unix timestamp in seconds when this token expires and becomes invalid</p></div></div></div></td></tr></tbody></table>

**400**

Bad request — invalid or missing parameters, expired/revoked privileges, or insufficient subscription

**401**

Unauthorized — client authentication failed

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

`{  -   "grant_type": "client_credentials",      -   "client_id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",      -   "client_secret": "Ex4mpleS3cret-DoNotUse"       }`

### Response samples

-   200
-   400
-   401

Content type

application/json

Copy

`{  -   "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJtb3JuaW5nIiwiaWF0IjoxNzcxMzEzNzI3LCJleHAiOjE3NzEzMTczMjcsImVudiI6InByb2QiLCJzdWIiOiJhMWIyYzNkNC1lNWY2LTRhN2ItOGM5ZC0wZTFmMmEzYjRjNWQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJhY2NvdW50SWQiOiIwMDAwMDAwMC0wMDAwLTQwMDAtODAwMC0wMDAwMDAwMDAwMDEiLCJyZXNvdXJjZUlkIjoiMDAwMDAwMDAtMDAwMC00MDAwLTgwMDAtMDAwMDAwMDAwMDAyIiwiYXBwSWQiOiJidXNpbmVzcyIsImF1ZCI6ImJ1c2luZXNzOjAwMDAwMDAwLTAwMDAtNDAwMC04MDAwLTAwMDAwMDAwMDAwMiIsInJvbGUiOjUwLCJzY29wZXMiOiIifQ.dGhpcy1pcy1hLXNhbXBsZS1zaWduYXR1cmU",      -   "tokenType": "Bearer",      -   "expiresAt": 1771317327// 2026-02-17 08:35:27 UTC       }`

## Documents

Create and manage business documents such as invoices, receipts, quotes, credit notes, and more.

Each document is associated with a specific business and includes income rows, payment rows, and client information.

## Add Document

post/documents

posthttps://api.greeninvoice.co.il/api/v1/documentsProductionSandbox

Add a document to the current business.

The document will be generated based on the default business and document settings, and by any overriding request attributes received in this endpoint.

**Notes:**

-   **VAT Configuration** — When declaring your `vatType`, you can define the general VAT type of the entire document, as well as the `vatType` for each individual income row.
-   **Document Linking** — Use `linkedDocumentIds` to state the related documents. For example, when creating a receipt, include the original invoice document ID in this array. This linkage enables the system to automatically mark the original invoice as closed.
-   **Payment Association** — The `linkedPaymentId` field allows you to define the payment ID that the document is relevant to. This can be attached only to invoice documents (type `305`).

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="type"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">type</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document type code.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>10</td><td>הצעת מחיר</td></tr><tr><td>20</td><td>חשבון / אישור תשלום</td></tr><tr><td>100</td><td>הזמנה</td></tr><tr><td>200</td><td>תעודת משלוח</td></tr><tr><td>210</td><td>תעודת החזרה</td></tr><tr><td>300</td><td>חשבון עסקה</td></tr><tr><td>305</td><td>חשבונית מס</td></tr><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>330</td><td>חשבונית זיכוי</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr><tr><td>410</td><td>ביטול תרומה</td></tr><tr><td>500</td><td>הזמנת רכש</td></tr><tr><td>600</td><td>קבלת פיקדון</td></tr><tr><td>610</td><td>משיכת פיקדון</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="lang"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">lang</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Lang)</span></div><div><span class="sc-Nxspf lmPA-Dn">Enum:</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"he"</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"en"</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Content language</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currency"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currency</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Currency)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>3-letter ISO currency code.</p><table><thead><tr><th>Code</th><th>Name</th></tr></thead><tbody><tr><td>ILS</td><td>שקל</td></tr><tr><td>USD</td><td>דולר</td></tr><tr><td>EUR</td><td>אירו</td></tr><tr><td>GBP</td><td>ליש״ט</td></tr><tr><td>JPY</td><td>יין יפני</td></tr><tr><td>CHF</td><td>פרנק שוויצרי</td></tr><tr><td>CNY</td><td>יואן סיני</td></tr><tr><td>AUD</td><td>דולר אוסטרלי</td></tr><tr><td>CAD</td><td>דולר קנדי</td></tr><tr><td>RUB</td><td>רובל</td></tr><tr><td>BRL</td><td>ריאל ברזילאי</td></tr><tr><td>HKD</td><td>דולר הונג קונגי</td></tr><tr><td>SGD</td><td>דולר סינגפורי</td></tr><tr><td>THB</td><td>באט תאילנדי</td></tr><tr><td>MXN</td><td>פזו מקסיקני</td></tr><tr><td>TRY</td><td>לירה טורקית</td></tr><tr><td>NZD</td><td>דולר ניו זילנדי</td></tr><tr><td>SEK</td><td>כתר שבדי</td></tr><tr><td>NOK</td><td>כתר נורבגי</td></tr><tr><td>DKK</td><td>כתר דני</td></tr><tr><td>KRW</td><td>וון דרום קוריאני</td></tr><tr><td>INR</td><td>רופי הודי</td></tr><tr><td>IDR</td><td>רופי אינדונזי</td></tr><tr><td>PLN</td><td>זלוטי</td></tr><tr><td>RON</td><td>לאו רומני</td></tr><tr><td>ZAR</td><td>ראנד דרא״פ</td></tr><tr><td>HRK</td><td>קונה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="vatType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">vatType</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentVatType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document-level VAT type.</p><table><thead><tr><th>Value</th><th>Meaning</th></tr></thead><tbody><tr><td>0</td><td>Default (based on business type)</td></tr><tr><td>1</td><td>Exempt (VAT-free)</td></tr><tr><td>2</td><td>Mixed (contains both exempt and taxable rows)</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="income"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand income"><span class="property-name">income</span></button><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (IncomeRowRequest)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Income rows</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document description. For example: <code>Just an order</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="remarks"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">remarks</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document remarks. For example: <code>Some remarks</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="footer"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">footer</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document footer text. For example: <code>Texts in footer</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="emailContent"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">emailContent</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Custom extra text appearing in the email sent to the customer. For example: <code>Email content</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="date"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">date</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document date in the format <code>YYYY-MM-DD</code>. Defaults to today. For example: <code>2026-05-12</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="dueDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">dueDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document payment due date in the format <code>YYYY-MM-DD</code>. For example: <code>2026-05-31</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="discount"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand discount"><span class="property-name">discount</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DiscountRequest)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="rounding"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">rounding</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><span class="sc-Nxspf lmPA-Dn">Default: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">false</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Round the amounts. Defaults to <code>false</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="signed"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">signed</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><span class="sc-Nxspf lmPA-Dn">Default: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">true</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Digitally sign the document. Defaults to <code>true</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="attachment"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">attachment</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><span class="sc-Nxspf lmPA-Dn">Default: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">false</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Attach the document in the email sent to the recipient. Defaults to <code>false</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="paymentRequestData"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand paymentRequestData"><span class="property-name">paymentRequestData</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Payment request configuration</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="client"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand client"><span class="property-name">client</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Client information</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="payment"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand payment"><span class="property-name">payment</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (PaymentRowRequest)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Payment rows</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="linkedDocumentIds"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">linkedDocumentIds</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Linked document IDs. When creating a receipt, include the original invoice document ID — this will automatically close the original invoice if needed. For example: <code>["031e827a-c664-c1e4-d231-a80027271123"]</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="linkedPaymentId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">linkedPaymentId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Linked payment ID. Can only be attached to invoice documents (type <code>305</code>). For example: <code>031e827a-c664-c1e4-d231-a80027271123</code>.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="linkType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">linkType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Reference type (applicable only when using <code>linkedDocumentIds</code>).</p><table><thead><tr><th>Value</th><th>Meaning</th></tr></thead><tbody><tr><td><code>link</code></td><td>Document is related to another</td></tr><tr><td><code>cancel</code></td><td>Document cancels another</td></tr></tbody></table></div></div></div></td></tr></tbody></table>

### Responses

**201**

Document created successfully

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

Expand all Collapse all

`{  -   "description": "Just an order",      -   "remarks": "Some remarks",      -   "footer": "Texts in footer",      -   "emailContent": "Email content",      -   "type": 305,      -   "date": "2026-05-12",      -   "dueDate": "2026-05-31",      -   "lang": "he",      -   "currency": "ILS",      -   "vatType": 0,      -   "discount": {          -   "amount": 1,              -   "type": "sum"                   },      -   "rounding": false,      -   "signed": true,      -   "attachment": false,      -   "paymentRequestData": {          -   "plugins": [                  -   {                          -   "id": "031e827a-c664-c1e4-d231-a80027271123",                              -   "group": 100,                              -   "type": 12100                                           }                               ],              -   "maxPayments": 1                   },      -   "client": {          -   "id": "7944827a-c664-11e4-8231-080027271114",              -   "name": "John Doe",              -   "emails": [                  -   "email1@example.com",                      -   "email2@example.com"                               ],              -   "taxId": "0123456789",              -   "address": "1 Luria St",              -   "city": "Tel Aviv",              -   "zip": "1234567",              -   "country": "IL",              -   "phone": "+972-54-1234567",              -   "fax": "+972-54-1234567",              -   "mobile": "+972-54-1234567",              -   "add": false,              -   "self": false                   },      -   "income": [          -   {                  -   "catalogNum": "MXDFSDD",                      -   "description": "Item description",                      -   "quantity": 1,                      -   "price": 300,                      -   "currency": "ILS",                      -   "currencyRate": 1,                      -   "vatRate": 0.18,                      -   "itemId": "8b338c95-095e-46d4-b2c6-331747508759",                      -   "vatType": 1                               }                   ],      -   "payment": [          -   {                  -   "date": "2026-05-21",                      -   "type": 3,                      -   "price": 300,                      -   "currency": "ILS",                      -   "currencyRate": 1,                      -   "bankName": "My Bank",                      -   "bankBranch": "198",                      -   "bankAccount": "212435",                      -   "chequeNum": "10002",                      -   "accountId": "TFGFFGSYYE",                      -   "transactionId": "TGBBBXNLKS75SKJS",                      -   "appType": 1,                      -   "subType": 1,                      -   "cardType": 2,                      -   "cardNum": "8765",                      -   "dealType": 1,                      -   "numPayments": 1,                      -   "firstPayment": 10                               }                   ],      -   "linkedDocumentIds": [          -   "031e827a-c664-c1e4-d231-a80027271123"                   ],      -   "linkedPaymentId": "031e827a-c664-c1e4-d231-a80027271123",      -   "linkType": "link"       }`

### Response samples

-   201

Content type

application/json

Copy

Expand all Collapse all

`{  -   "id": "57ae2ff9-0c24-43e8-b39c-a5bdcc05573d",      -   "number": 40034,      -   "dueDate": "2026-05-31",      -   "type": 305,      -   "signed": true,      -   "lang": "he",      -   "client": {          -   "id": "7944827a-c664-11e4-8231-080027271114"                   },      -   "taxAuthorityConfirmationInitiated": false,      -   "url": {          -   "origin": "string",              -   "he": "string",              -   "en": "string"                   },      -   "taxAuthorityConfirmationLastError": 0,      -   "vatRate": 0.18       }`

## Search Documents

post/documents/search

posthttps://api.greeninvoice.co.il/api/v1/documents/searchProductionSandbox

Search the documents of the current business using any combination of the filters in the request body. All filters are optional; omitting the body returns the most recent documents. Results are paginated.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### Request Body schema: application/json

optional

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="page"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">page</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><span class="sc-Nxspf lmPA-Dn">Default: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">1</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Page number to retrieve. Defaults to 1.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pageSize"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pageSize</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><span class="sc-Nxspf lmPA-Dn">Default: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">25</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Number of results per page. Defaults to 25.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="number"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">number</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by document serial number. For example: 12001.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="type"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">type</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integers</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by document type(s).</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>10</td><td>הצעת מחיר</td></tr><tr><td>20</td><td>חשבון / אישור תשלום</td></tr><tr><td>100</td><td>הזמנה</td></tr><tr><td>200</td><td>תעודת משלוח</td></tr><tr><td>210</td><td>תעודת החזרה</td></tr><tr><td>300</td><td>חשבון עסקה</td></tr><tr><td>305</td><td>חשבונית מס</td></tr><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>330</td><td>חשבונית זיכוי</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr><tr><td>410</td><td>ביטול תרומה</td></tr><tr><td>500</td><td>הזמנת רכש</td></tr><tr><td>600</td><td>קבלת פיקדון</td></tr><tr><td>610</td><td>משיכת פיקדון</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="status"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">status</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integers</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentStatus)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by document status(es).</p><table><thead><tr><th>Code</th><th>Status</th></tr></thead><tbody><tr><td>0</td><td>מסמך פתוח</td></tr><tr><td>1</td><td>מסמך סגור</td></tr><tr><td>2</td><td>מסמך סומן ידנית כסגור</td></tr><tr><td>3</td><td>מסמך מבטל</td></tr><tr><td>4</td><td>מסמך שבוטל</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentTypes"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentTypes</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integers</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (PaymentGroup)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by payment type(s) used in the document.</p><table><thead><tr><th>Code</th><th>Method</th></tr></thead><tbody><tr><td>0</td><td>ניכוי במקור</td></tr><tr><td>1</td><td>מזומן</td></tr><tr><td>2</td><td>צ׳ק</td></tr><tr><td>3</td><td>כרטיס אשראי</td></tr><tr><td>4</td><td>העברה בנקאית</td></tr><tr><td>5</td><td>פייפאל</td></tr><tr><td>10</td><td>אפליקציית תשלום</td></tr><tr><td>11</td><td>אחר</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="fromDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">fromDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Return documents whose document date from this date, in the format <code>YYYY-MM-DD</code>. For example: <code>2016-01-01</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="toDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">toDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Return documents whose document date to this date, in the format <code>YYYY-MM-DD</code>. For example: <code>2016-01-31</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="clientId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">clientId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by client ID. For example: <code>28fa4c1d-a29b-11e4-963c-18002725111e</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="clientName"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">clientName</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by client name. For example: <code>John</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by document description. For example: <code>Any text</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="download"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">download</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by whether the document was downloaded by the client. For example: <code>true</code>.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="sort"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">sort</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Field to sort the result set by.</p><table><thead><tr><th>Value</th><th>Sorts by</th></tr></thead><tbody><tr><td><code>documentDate</code></td><td>Document (issue) date</td></tr><tr><td><code>dueDate</code></td><td>Due date</td></tr><tr><td><code>client</code></td><td>Client name</td></tr></tbody></table></div></div></div></td></tr></tbody></table>

### Responses

**200**

Paginated list of documents matching the search

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="total"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">total</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total number of documents matching the search</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="page"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">page</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The requested page number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pageSize"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pageSize</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The requested page size</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="from"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">from</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Index of the first item in the current page</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="to"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">to</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Index of the last item in the current page</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pages"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pages</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total number of pages available</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="items"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand items"><span class="property-name">items</span></button><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (SearchDocument)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The documents matching the search</p></div></div></div></td></tr></tbody></table>

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

Expand all Collapse all

`{  -   "page": 1,      -   "pageSize": 25,      -   "number": 12001,      -   "type": [          -   305                   ],      -   "status": [          -   0                   ],      -   "paymentTypes": [          -   3                   ],      -   "fromDate": "2016-01-01",      -   "toDate": "2016-01-31",      -   "clientId": "28fa4c1d-a29b-11e4-963c-18002725111e",      -   "clientName": "John",      -   "description": "Any text",      -   "download": true,      -   "sort": "documentDate"       }`

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`{  -   "total": 25,      -   "page": 1,      -   "pageSize": 25,      -   "from": 1,      -   "to": 25,      -   "pages": 2,      -   "items": [          -   {                  -   "id": "73aedf13-0263-4399-95b8-2261e1c89e68",                      -   "type": 305,                      -   "number": "80010",                      -   "status": 0,                      -   "documentDate": "2026-01-19",                      -   "creationDate": 1768829547,// 2026-01-19 13:32:27 UTC                      -   "lang": "he",                      -   "description": "Just an order",                      -   "remarks": "Some remarks",                      -   "amount": 354,                      -   "amountLocal": 354,                      -   "amountDueVat": 300,                      -   "amountExemptVat": 0,                      -   "amountExcludeVat": 0,                      -   "amountOpened": 0,                      -   "vat": 54,                      -   "vatType": 0,                      -   "vatRate": 0.18,                      -   "currency": "ILS",                      -   "currencyRate": 1,                      -   "client": {                          -   "id": "b0077e19-977b-4389-a2e1-f84fa0527d23",                              -   "name": "John Doe",                              -   "emails": [                                  -   "email1@example.com"                                                       ],                              -   "taxId": "0123456789",                              -   "self": false,                              -   "country": "IL",                              -   "phone": "+972-54-1234567"                                           },                      -   "business": {                          -   "type": 1,                              -   "exemption": false                                           },                      -   "data": {                          -   "tags": [ ],                              -   "taxAuthorityConfirmationNumber": "20241104100000000000001",                              -   "taxAuthorityConfirmationLastError": 0                                           },                      -   "income": [                          -   {                                  -   "catalogNum": "MXDFSDD",                                      -   "description": "Item description",                                      -   "quantity": 1,                                      -   "price": 300,                                      -   "currency": "ILS",                                      -   "currencyRate": 1,                                      -   "vatType": 1,                                      -   "vatRate": 0.18,                                      -   "amount": 300,                                      -   "vat": 54,                                      -   "amountTotal": 354,                                      -   "itemId": "8b338c95-095e-46d4-b2c6-331747508759"                                                       }                                           ],                      -   "payment": [                          -   {                                  -   "name": "כרטיס אשראי",                                      -   "type": 3,                                      -   "subType": 1,                                      -   "appType": 1,                                      -   "price": 300,                                      -   "currency": "ILS",                                      -   "ref": [                                          -   305                                                                   ],                                      -   "cancellable": false                                                       }                                           ],                      -   "signed": true,                      -   "cancellable": true,                      -   "downloaded": false,                      -   "reverseCharge": false,                      -   "rounding": false,                      -   "taxConfirmationEligible": false,                      -   "url": {                          -   "he": "string",                              -   "origin": "string",                              -   "en": "string"                                           }                               }                   ]       }`

## Search Payments in Documents

post/documents/payments/search

posthttps://api.greeninvoice.co.il/api/v1/documents/payments/searchProductionSandbox

Search the payments recorded across the current business's documents, using any combination of the filters in the request body. Each result is the document that contains the matching payment(s), with the payments in its `payment` array. All filters are optional. Results are paginated.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### Request Body schema: application/json

optional

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="page"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">page</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><span class="sc-Nxspf lmPA-Dn">Default: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">1</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Page number to retrieve. Defaults to 1.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pageSize"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pageSize</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><span class="sc-Nxspf lmPA-Dn">Default: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">25</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Number of results per page. Defaults to 25.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="type"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">type</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integers</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (PaymentSearchDocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by document type(s).</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr><tr><td>600</td><td>קבלת פיקדון</td></tr><tr><td>610</td><td>משיכת פיקדון</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentTypes"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentTypes</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integers</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (PaymentGroup)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by payment type(s) used in the document.</p><table><thead><tr><th>Code</th><th>Method</th></tr></thead><tbody><tr><td>0</td><td>ניכוי במקור</td></tr><tr><td>1</td><td>מזומן</td></tr><tr><td>2</td><td>צ׳ק</td></tr><tr><td>3</td><td>כרטיס אשראי</td></tr><tr><td>4</td><td>העברה בנקאית</td></tr><tr><td>5</td><td>פייפאל</td></tr><tr><td>10</td><td>אפליקציית תשלום</td></tr><tr><td>11</td><td>אחר</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="fromDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">fromDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Return payments dated on or after this date, in the format <code>YYYY-MM-DD</code>. For example: <code>2016-01-01</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="toDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">toDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Return payments dated on or before this date, in the format <code>YYYY-MM-DD</code>. For example: <code>2016-01-31</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Payment identifier, such as a cheque number or PayPal transaction ID. For example: <code>427547</code>.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="sort"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">sort</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Field and direction to sort the result set by.</p><table><thead><tr><th>Value</th><th>Sorts by</th></tr></thead><tbody><tr><td><code>date:desc</code></td><td>Payment date, descending</td></tr><tr><td><code>date:asc</code></td><td>Payment date, ascending</td></tr></tbody></table></div></div></div></td></tr></tbody></table>

### Responses

**200**

Paginated list of documents whose payments matched the search

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="total"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">total</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total number of documents matching the search</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="page"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">page</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The requested page number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pageSize"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pageSize</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The requested page size</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="from"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">from</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Index of the first item in the current page</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="to"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">to</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Index of the last item in the current page</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pages"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pages</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total number of pages available</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="items"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand items"><span class="property-name">items</span></button><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentPayment)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The documents whose payments matched the search</p></div></div></div></td></tr></tbody></table>

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

Expand all Collapse all

`{  -   "page": 1,      -   "pageSize": 25,      -   "type": [          -   320                   ],      -   "paymentTypes": [          -   3                   ],      -   "fromDate": "2016-01-01",      -   "toDate": "2016-01-31",      -   "paymentId": "427547",      -   "sort": "date:desc"       }`

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`{  -   "total": 25,      -   "page": 1,      -   "pageSize": 25,      -   "from": 1,      -   "to": 25,      -   "pages": 2,      -   "items": [          -   {                  -   "id": "7af2e6e7-6551-4691-9e80-a5e6172e81cc",                      -   "type": 305,                      -   "number": 60005,                      -   "status": 0,                      -   "documentDate": "2025-12-14T00:00:00",                      -   "creationDate": "2025-12-14T09:39:03",                      -   "lang": "he",                      -   "amount": 354,                      -   "amountLocal": 354,                      -   "amountDueVat": 300,                      -   "amountExemptVat": 0,                      -   "amountExcludeVat": 0,                      -   "vat": 54,                      -   "currency": "ILS",                      -   "currencyRate": 1,                      -   "client": {                          -   "id": "b0077e19-977b-4389-a2e1-f84fa0527d23",                              -   "name": "John Doe",                              -   "emails": [                                  -   "email1@example.com"                                                       ],                              -   "taxId": "0123456789",                              -   "self": false,                              -   "country": "IL",                              -   "phone": "+972-54-1234567"                                           },                      -   "business": {                          -   "type": 1,                              -   "exemption": false                                           },                      -   "income": [                          -   {                                  -   "catalogNum": "MXDFSDD",                                      -   "description": "Item description",                                      -   "quantity": 1,                                      -   "price": 300,                                      -   "currency": "ILS",                                      -   "currencyRate": 1,                                      -   "vatType": 1,                                      -   "vatRate": 0.18,                                      -   "amount": 300,                                      -   "vat": 54,                                      -   "amountTotal": 354,                                      -   "itemId": "8b338c95-095e-46d4-b2c6-331747508759"                                                       }                                           ],                      -   "payment": [                          -   {                                  -   "id": "63dad8e3-44d2-40b4-8708-39e6c37d0448",                                      -   "date": "2025-12-14T00:00:00",                                      -   "type": 3,                                      -   "paymentStatus": 0,                                      -   "price": 251,                                      -   "amount": 251,                                      -   "currency": "ILS",                                      -   "currencyRate": 1,                                      -   "name": "כרטיס אשראי",                                      -   "description": "ויזה 0000 / רגיל",                                      -   "cardType": 2,                                      -   "cardNum": "0000",                                      -   "dealType": 1,                                      -   "numPayments": 1                                                       }                                           ],                      -   "signed": true,                      -   "cancellable": true,                      -   "downloaded": false,                      -   "reverseCharge": false,                      -   "rounding": false,                      -   "taxConfirmationEligible": false,                      -   "url": {                          -   "he": "string",                              -   "origin": "string"                                           }                               }                   ]       }`

## Get a Preview Document

post/documents/preview

posthttps://api.greeninvoice.co.il/api/v1/documents/previewProductionSandbox

Previews a document before the actual generation.

This endpoint returns a file in Base64 format (you can read more about Base64 [here](https://en.wikipedia.org/wiki/Base64)).

If you would like to view the file on your website there are built-in plugins to display PDF, other than that - if you would like to have a consistent user experience through all browsers (including mobile browsers) we would suggest using [PDF.js](https://mozilla.github.io/pdf.js/) (an amazing Mozilla library), which can view PDF from Base64 format.

If you would like to add a download button for the preview in your website, here is a simple script to do that (do not forget to switch the {base64string} with the Base64 file that you received from the result):

```
<a download="preview-document.pdf" href="data:application/pdf;base64,{base64string}">Download Preview</a>
```

**NOTE:** If you would like just to check how a preview file looks, use the string that was given in the `file` property from our server response, put it in the following website: [https://www.freeformatter.com/base64-encoder.html](https://www.freeformatter.com/base64-encoder.html) and click `DECODE AND DOWNLOAD`. This will download the base64 string as a PDF file into your computer so that you can view it.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="type"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">type</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document type code.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>10</td><td>הצעת מחיר</td></tr><tr><td>20</td><td>חשבון / אישור תשלום</td></tr><tr><td>100</td><td>הזמנה</td></tr><tr><td>200</td><td>תעודת משלוח</td></tr><tr><td>210</td><td>תעודת החזרה</td></tr><tr><td>300</td><td>חשבון עסקה</td></tr><tr><td>305</td><td>חשבונית מס</td></tr><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>330</td><td>חשבונית זיכוי</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr><tr><td>410</td><td>ביטול תרומה</td></tr><tr><td>500</td><td>הזמנת רכש</td></tr><tr><td>600</td><td>קבלת פיקדון</td></tr><tr><td>610</td><td>משיכת פיקדון</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="lang"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">lang</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Lang)</span></div><div><span class="sc-Nxspf lmPA-Dn">Enum:</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"he"</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"en"</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Content language</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currency"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currency</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Currency)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>3-letter ISO currency code.</p><table><thead><tr><th>Code</th><th>Name</th></tr></thead><tbody><tr><td>ILS</td><td>שקל</td></tr><tr><td>USD</td><td>דולר</td></tr><tr><td>EUR</td><td>אירו</td></tr><tr><td>GBP</td><td>ליש״ט</td></tr><tr><td>JPY</td><td>יין יפני</td></tr><tr><td>CHF</td><td>פרנק שוויצרי</td></tr><tr><td>CNY</td><td>יואן סיני</td></tr><tr><td>AUD</td><td>דולר אוסטרלי</td></tr><tr><td>CAD</td><td>דולר קנדי</td></tr><tr><td>RUB</td><td>רובל</td></tr><tr><td>BRL</td><td>ריאל ברזילאי</td></tr><tr><td>HKD</td><td>דולר הונג קונגי</td></tr><tr><td>SGD</td><td>דולר סינגפורי</td></tr><tr><td>THB</td><td>באט תאילנדי</td></tr><tr><td>MXN</td><td>פזו מקסיקני</td></tr><tr><td>TRY</td><td>לירה טורקית</td></tr><tr><td>NZD</td><td>דולר ניו זילנדי</td></tr><tr><td>SEK</td><td>כתר שבדי</td></tr><tr><td>NOK</td><td>כתר נורבגי</td></tr><tr><td>DKK</td><td>כתר דני</td></tr><tr><td>KRW</td><td>וון דרום קוריאני</td></tr><tr><td>INR</td><td>רופי הודי</td></tr><tr><td>IDR</td><td>רופי אינדונזי</td></tr><tr><td>PLN</td><td>זלוטי</td></tr><tr><td>RON</td><td>לאו רומני</td></tr><tr><td>ZAR</td><td>ראנד דרא״פ</td></tr><tr><td>HRK</td><td>קונה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="vatType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">vatType</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentVatType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document-level VAT type.</p><table><thead><tr><th>Value</th><th>Meaning</th></tr></thead><tbody><tr><td>0</td><td>Default (based on business type)</td></tr><tr><td>1</td><td>Exempt (VAT-free)</td></tr><tr><td>2</td><td>Mixed (contains both exempt and taxable rows)</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="income"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand income"><span class="property-name">income</span></button><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (IncomeRowRequest)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Income rows</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document description. For example: <code>Just an order</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="remarks"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">remarks</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document remarks. For example: <code>Some remarks</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="footer"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">footer</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document footer text. For example: <code>Texts in footer</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="emailContent"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">emailContent</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Custom extra text appearing in the email sent to the customer. For example: <code>Email content</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="date"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">date</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document date in the format <code>YYYY-MM-DD</code>. Defaults to today. For example: <code>2026-05-12</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="dueDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">dueDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document payment due date in the format <code>YYYY-MM-DD</code>. For example: <code>2026-05-31</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="discount"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand discount"><span class="property-name">discount</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DiscountRequest)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="rounding"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">rounding</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><span class="sc-Nxspf lmPA-Dn">Default: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">false</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Round the amounts. Defaults to <code>false</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="signed"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">signed</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><span class="sc-Nxspf lmPA-Dn">Default: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">true</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Digitally sign the document. Defaults to <code>true</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="attachment"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">attachment</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><span class="sc-Nxspf lmPA-Dn">Default: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">false</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Attach the document in the email sent to the recipient. Defaults to <code>false</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="paymentRequestData"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand paymentRequestData"><span class="property-name">paymentRequestData</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Payment request configuration</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="client"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand client"><span class="property-name">client</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Client information</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="payment"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand payment"><span class="property-name">payment</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (PaymentRowRequest)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Payment rows</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="linkedDocumentIds"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">linkedDocumentIds</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Linked document IDs. When creating a receipt, include the original invoice document ID — this will automatically close the original invoice if needed. For example: <code>["031e827a-c664-c1e4-d231-a80027271123"]</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="linkedPaymentId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">linkedPaymentId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Linked payment ID. Can only be attached to invoice documents (type <code>305</code>). For example: <code>031e827a-c664-c1e4-d231-a80027271123</code>.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="linkType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">linkType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Reference type (applicable only when using <code>linkedDocumentIds</code>).</p><table><thead><tr><th>Value</th><th>Meaning</th></tr></thead><tbody><tr><td><code>link</code></td><td>Document is related to another</td></tr><tr><td><code>cancel</code></td><td>Document cancels another</td></tr></tbody></table></div></div></div></td></tr></tbody></table>

### Responses

**200**

Preview document generated successfully

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="file"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">file</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;byte&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The generated preview document as a Base64-encoded PDF string. See the endpoint description for guidance on decoding and rendering.</p></div></div></div></td></tr></tbody></table>

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

Expand all Collapse all

`{  -   "description": "Just an order",      -   "remarks": "Some remarks",      -   "footer": "Texts in footer",      -   "emailContent": "Email content",      -   "type": 305,      -   "date": "2026-05-12",      -   "dueDate": "2026-05-31",      -   "lang": "he",      -   "currency": "ILS",      -   "vatType": 0,      -   "discount": {          -   "amount": 1,              -   "type": "sum"                   },      -   "rounding": false,      -   "signed": true,      -   "attachment": false,      -   "paymentRequestData": {          -   "plugins": [                  -   {                          -   "id": "031e827a-c664-c1e4-d231-a80027271123",                              -   "group": 100,                              -   "type": 12100                                           }                               ],              -   "maxPayments": 1                   },      -   "client": {          -   "id": "7944827a-c664-11e4-8231-080027271114",              -   "name": "John Doe",              -   "emails": [                  -   "email1@example.com",                      -   "email2@example.com"                               ],              -   "taxId": "0123456789",              -   "address": "1 Luria St",              -   "city": "Tel Aviv",              -   "zip": "1234567",              -   "country": "IL",              -   "phone": "+972-54-1234567",              -   "fax": "+972-54-1234567",              -   "mobile": "+972-54-1234567",              -   "add": false,              -   "self": false                   },      -   "income": [          -   {                  -   "catalogNum": "MXDFSDD",                      -   "description": "Item description",                      -   "quantity": 1,                      -   "price": 300,                      -   "currency": "ILS",                      -   "currencyRate": 1,                      -   "vatRate": 0.18,                      -   "itemId": "8b338c95-095e-46d4-b2c6-331747508759",                      -   "vatType": 1                               }                   ],      -   "payment": [          -   {                  -   "date": "2026-05-21",                      -   "type": 3,                      -   "price": 300,                      -   "currency": "ILS",                      -   "currencyRate": 1,                      -   "bankName": "My Bank",                      -   "bankBranch": "198",                      -   "bankAccount": "212435",                      -   "chequeNum": "10002",                      -   "accountId": "TFGFFGSYYE",                      -   "transactionId": "TGBBBXNLKS75SKJS",                      -   "appType": 1,                      -   "subType": 1,                      -   "cardType": 2,                      -   "cardNum": "8765",                      -   "dealType": 1,                      -   "numPayments": 1,                      -   "firstPayment": 10                               }                   ],      -   "linkedDocumentIds": [          -   "031e827a-c664-c1e4-d231-a80027271123"                   ],      -   "linkedPaymentId": "031e827a-c664-c1e4-d231-a80027271123",      -   "linkType": "link"       }`

### Response samples

-   200

Content type

application/json

Copy

`{  -   "file": "JVBERi0xLjcKJeLjz9MKMyAwIG9iago8PC9UeXBlIC9QYWdlCi9QYXJlbnQgMSAwIFIK..."       }`

## Get Document Information

get/documents/info

gethttps://api.greeninvoice.co.il/api/v1/documents/info?type={type}ProductionSandbox

Retrieve metadata about a specific document type — the next document number to assign, supported features (income rows, payment rows, self-invoicing, linked-document flows), default business settings that apply when creating documents of this type, and the payment plugins active on this business.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### query Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="type"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">type</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentType)</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">type=305</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document type to retrieve information for</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Document type information retrieved successfully

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="type"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">type</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document type code.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>10</td><td>הצעת מחיר</td></tr><tr><td>20</td><td>חשבון / אישור תשלום</td></tr><tr><td>100</td><td>הזמנה</td></tr><tr><td>200</td><td>תעודת משלוח</td></tr><tr><td>210</td><td>תעודת החזרה</td></tr><tr><td>300</td><td>חשבון עסקה</td></tr><tr><td>305</td><td>חשבונית מס</td></tr><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>330</td><td>חשבונית זיכוי</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr><tr><td>410</td><td>ביטול תרומה</td></tr><tr><td>500</td><td>הזמנת רכש</td></tr><tr><td>600</td><td>קבלת פיקדון</td></tr><tr><td>610</td><td>משיכת פיקדון</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="number"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">number</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Next document number that will be assigned to a new document of this <code>type</code> in the business's series</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="footer"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand footer"><span class="property-name">footer</span></button><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document footer text, keyed by language. Either or both keys may be present depending on the business's configuration.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="remark"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand remark"><span class="property-name">remark</span></button><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document remark text, keyed by language. Either or both keys may be present depending on the business's configuration.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="used"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">used</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether the business has previously issued at least one document of this <code>type</code></p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="first"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">first</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether this would be the first document of this <code>type</code> for the business</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="lastDocumentDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">lastDocumentDate</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Date of the most recent document of this <code>type</code> issued by the business, in the format <code>YYYY-MM-DD</code></p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="today"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">today</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Today's date in the business's timezone, in the format <code>YYYY-MM-DD</code></p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="settings"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand settings"><span class="property-name">settings</span></button><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Business-level defaults that apply when creating a new document of this <code>type</code></p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="selfInvoiceEnabled"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">selfInvoiceEnabled</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether the business may issue self-invoices for this document type</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="incomeRowsEnabled"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">incomeRowsEnabled</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether income rows are supported on this document type</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="incomeRowsRequired"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">incomeRowsRequired</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether income rows are required on this document type</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentRowsEnabled"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentRowsEnabled</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether payment rows are supported on this document type</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="reverseCharge"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">reverseCharge</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether reverse-charge VAT applies to this document</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="payable"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">payable</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether this document type accepts payments</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="exemption"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">exemption</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether the business is exempt from VAT</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="vatRate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">vatRate</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>VAT rate that will apply to a new document, expressed as a decimal fraction (e.g. 0.18 for 18%)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="vatTypes"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">vatTypes</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integers</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentVatType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>VAT types available for use on this document</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="paymentPlugins"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand paymentPlugins"><span class="property-name">paymentPlugins</span></button><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Plugin)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Active payment plugins available to this business for documents of this type</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="hasTaxAuthorityConfirmation"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">hasTaxAuthorityConfirmation</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether this document type requires Tax Authority confirmation in this business's type</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="linkedDocumentIds"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">linkedDocumentIds</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt; </span><span class="sc-Nxspf sc-cfxfcM sc-kAkpmW lmPA-Dn hHOUkK hXkwsT">[ items<span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid &gt;</span> ]</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Returned only when the request is part of a linked-document flow (e.g. creating a receipt from an invoice). The IDs of the documents being linked.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="linkedPaymentId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">linkedPaymentId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Returned only when the request is part of a linked-document flow. The ID of the payment being linked.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="linkType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">linkType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentLinkType)</span></div><div><span class="sc-Nxspf lmPA-Dn">Enum:</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"copy"</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"link"</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"cancel"</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Relationship type between a document and its linked documents.</p><table><thead><tr><th>Value</th><th>Meaning</th></tr></thead><tbody><tr><td>copy</td><td>A new document duplicating an existing document's contents</td></tr><tr><td>link</td><td>A reference to a related document (e.g. an invoice → receipt link)</td></tr><tr><td>cancel</td><td>A document that cancels or credits an existing document</td></tr></tbody></table></div></div></div></td></tr></tbody></table>

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl 'https://api.greeninvoice.co.il/api/v1/documents/info?type=305' \
  -H "Authorization: Bearer $MORNING_ACCESS_TOKEN"
```

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`{  -   "type": 305,      -   "number": 50041,      -   "footer": {          -   "he": "string",              -   "en": "string"                   },      -   "remark": {          -   "he": "string",              -   "en": "string"                   },      -   "used": true,      -   "first": false,      -   "lastDocumentDate": "2026-05-18",      -   "today": "2026-06-04",      -   "settings": {          -   "documentCurrency": "ILS",              -   "documentLang": "he",              -   "documentRounding": false,              -   "documentVatType": 0,              -   "rowVatType": 1,              -   "mixedVatEnabled": true,              -   "receiptIncomeEnabled": false,              -   "unsignedEnabled": false,              -   "attachmentEnabled": true,              -   "selectedPaymentChannels": [                  -   100,                      -   120,                      -   150,                      -   160                               ],              -   "taxAuthorityProformaInvoiceEnabled": true,              -   "taxAuthorityConnected": false                   },      -   "selfInvoiceEnabled": true,      -   "incomeRowsEnabled": true,      -   "incomeRowsRequired": true,      -   "paymentRowsEnabled": false,      -   "reverseCharge": false,      -   "payable": true,      -   "exemption": false,      -   "vatRate": 0.18,      -   "vatTypes": [          -   0,              -   1,              -   2                   ],      -   "paymentPlugins": [          -   {                  -   "id": "9aa1a2ef-3efb-4566-b59a-54c233e81557",                      -   "description": "קארדקום",                      -   "friendlyName": "מסוף בדיקות (סליקה במערכת)",                      -   "active": true,                      -   "type": 12100,                      -   "maxPayments": 36,                      -   "creationDate": 1766492513,// 2025-12-23 12:21:53 UTC                      -   "lastUpdateDate": 1766492514// 2025-12-23 12:21:54 UTC                               }                   ],      -   "linkedDocumentIds": [          -   "497f6eca-6276-4993-bfeb-53cbbbba6f08"                   ],      -   "linkedPaymentId": "87314ac7-43f8-4e28-a371-6cca884d2972",      -   "linkType": "copy",      -   "hasTaxAuthorityConfirmation": false       }`

## Get Document Templates

get/documents/templates

gethttps://api.greeninvoice.co.il/api/v1/documents/templatesProductionSandbox

Retrieve information about the available document templates and their corresponding colour skins. Templates are global to the system; every business sees the same list.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

### Responses

**200**

List of available document templates

##### Response Schema: application/json

Array

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The template ID</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The name of the template</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>A description of the template — typically usage notes or recommended logo size</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="defaultSkinId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">defaultSkinId</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The default skin ID for this template</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="skins"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand skins"><span class="property-name">skins</span></button><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (TemplateSkin)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Available skins (colour variants) for this template</p></div></div></div></td></tr></tbody></table>

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl 'https://api.greeninvoice.co.il/api/v1/documents/templates' \
  -H "Authorization: Bearer $MORNING_ACCESS_TOKEN"
```

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`[  -   {          -   "id": 6,              -   "name": "דריי מרטיני",              -   "description": "כדי שהלוגו לא ייראה מפוקסל, מומלץ להעלות קובץ בגודל מינימלי של 450x300 פיקסלים.",              -   "defaultSkinId": 8,              -   "skins": [                  -   {                          -   "id": 1,                              -   "attributes": {                                  -   "color1": "#FF1919",                                      -   "color2": "#FFFFFF"                                                       }                                           }                               ]                   }       ]`

## Get Document Types

get/documents/types

gethttps://api.greeninvoice.co.il/api/v1/documents/types?lang={lang}ProductionSandbox

Retrieve the available document types as a list of `{ id, name }` pairs. Names are localised by the `lang` query parameter.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### query Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="lang"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">lang</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Lang)</span></div><div><span class="sc-Nxspf lmPA-Dn">Enum:</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"he"</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"en"</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">lang=he</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Content language for the localised <code>name</code> field. Defaults to <code>he</code> (Hebrew) if omitted or unsupported.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

List of available document types with localised names

##### Response Schema: application/json

Array

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document type code.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>10</td><td>הצעת מחיר</td></tr><tr><td>20</td><td>חשבון / אישור תשלום</td></tr><tr><td>100</td><td>הזמנה</td></tr><tr><td>200</td><td>תעודת משלוח</td></tr><tr><td>210</td><td>תעודת החזרה</td></tr><tr><td>300</td><td>חשבון עסקה</td></tr><tr><td>305</td><td>חשבונית מס</td></tr><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>330</td><td>חשבונית זיכוי</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr><tr><td>410</td><td>ביטול תרומה</td></tr><tr><td>500</td><td>הזמנת רכש</td></tr><tr><td>600</td><td>קבלת פיקדון</td></tr><tr><td>610</td><td>משיכת פיקדון</td></tr></tbody></table></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Localised name of the document type, in the language indicated by the <code>lang</code> query parameter</p></div></div></div></td></tr></tbody></table>

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl 'https://api.greeninvoice.co.il/api/v1/documents/types' \
  -H "Authorization: Bearer $MORNING_ACCESS_TOKEN"
```

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`[  -   {          -   "id": 305,              -   "name": "הצעת מחיר"                   }       ]`

## Get Document Statuses

get/documents/statuses

gethttps://api.greeninvoice.co.il/api/v1/documents/statuses?lang={lang}ProductionSandbox

Retrieve the available document statuses as a list of `{ id, name }` pairs. Names are localised by the `lang` query parameter.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### query Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="lang"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">lang</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Lang)</span></div><div><span class="sc-Nxspf lmPA-Dn">Enum:</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"he"</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"en"</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">lang=he</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Content language for the localised <code>name</code> field. Defaults to <code>he</code> (Hebrew) if omitted or unsupported.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

List of available document statuses with localised names

##### Response Schema: application/json

Array

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentStatus)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document status.</p><table><thead><tr><th>Code</th><th>Status</th></tr></thead><tbody><tr><td>0</td><td>מסמך פתוח</td></tr><tr><td>1</td><td>מסמך סגור</td></tr><tr><td>2</td><td>מסמך סומן ידנית כסגור</td></tr><tr><td>3</td><td>מסמך מבטל</td></tr><tr><td>4</td><td>מסמך שבוטל</td></tr></tbody></table></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Localised name of the document status, in the language indicated by the <code>lang</code> query parameter</p></div></div></div></td></tr></tbody></table>

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl 'https://api.greeninvoice.co.il/api/v1/documents/statuses' \
  -H "Authorization: Bearer $MORNING_ACCESS_TOKEN"
```

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`[  -   {          -   "id": 0,              -   "name": "מסמך פתוח"                   },      -   {          -   "id": 1,              -   "name": "מסמך סגור"                   },      -   {          -   "id": 2,              -   "name": "מסמך סומן ידנית כסגור"                   },      -   {          -   "id": 3,              -   "name": "מסמך מבטל"                   },      -   {          -   "id": 4,              -   "name": "מסמך שבוטל"                   }       ]`

## Get Document

get/documents/{id}

gethttps://api.greeninvoice.co.il/api/v1/documents/{id}ProductionSandbox

Retrieve a single document by its ID.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">57ae2ff9-0c24-43e8-b39c-a5bdcc05573d</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document ID</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Document retrieved successfully

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The document unique ID</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="type"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">type</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document type code.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>10</td><td>הצעת מחיר</td></tr><tr><td>20</td><td>חשבון / אישור תשלום</td></tr><tr><td>100</td><td>הזמנה</td></tr><tr><td>200</td><td>תעודת משלוח</td></tr><tr><td>210</td><td>תעודת החזרה</td></tr><tr><td>300</td><td>חשבון עסקה</td></tr><tr><td>305</td><td>חשבונית מס</td></tr><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>330</td><td>חשבונית זיכוי</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr><tr><td>410</td><td>ביטול תרומה</td></tr><tr><td>500</td><td>הזמנת רכש</td></tr><tr><td>600</td><td>קבלת פיקדון</td></tr><tr><td>610</td><td>משיכת פיקדון</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="number"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">number</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document serial number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="documentDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">documentDate</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document reference date in the format <code>YYYY-MM-DD</code></p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="status"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">status</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentStatus)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document status.</p><table><thead><tr><th>Code</th><th>Status</th></tr></thead><tbody><tr><td>0</td><td>מסמך פתוח</td></tr><tr><td>1</td><td>מסמך סגור</td></tr><tr><td>2</td><td>מסמך סומן ידנית כסגור</td></tr><tr><td>3</td><td>מסמך מבטל</td></tr><tr><td>4</td><td>מסמך שבוטל</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="lang"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">lang</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Lang)</span></div><div><span class="sc-Nxspf lmPA-Dn">Enum:</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"he"</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"en"</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Content language</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currency"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currency</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Currency)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>3-letter ISO currency code.</p><table><thead><tr><th>Code</th><th>Name</th></tr></thead><tbody><tr><td>ILS</td><td>שקל</td></tr><tr><td>USD</td><td>דולר</td></tr><tr><td>EUR</td><td>אירו</td></tr><tr><td>GBP</td><td>ליש״ט</td></tr><tr><td>JPY</td><td>יין יפני</td></tr><tr><td>CHF</td><td>פרנק שוויצרי</td></tr><tr><td>CNY</td><td>יואן סיני</td></tr><tr><td>AUD</td><td>דולר אוסטרלי</td></tr><tr><td>CAD</td><td>דולר קנדי</td></tr><tr><td>RUB</td><td>רובל</td></tr><tr><td>BRL</td><td>ריאל ברזילאי</td></tr><tr><td>HKD</td><td>דולר הונג קונגי</td></tr><tr><td>SGD</td><td>דולר סינגפורי</td></tr><tr><td>THB</td><td>באט תאילנדי</td></tr><tr><td>MXN</td><td>פזו מקסיקני</td></tr><tr><td>TRY</td><td>לירה טורקית</td></tr><tr><td>NZD</td><td>דולר ניו זילנדי</td></tr><tr><td>SEK</td><td>כתר שבדי</td></tr><tr><td>NOK</td><td>כתר נורבגי</td></tr><tr><td>DKK</td><td>כתר דני</td></tr><tr><td>KRW</td><td>וון דרום קוריאני</td></tr><tr><td>INR</td><td>רופי הודי</td></tr><tr><td>IDR</td><td>רופי אינדונזי</td></tr><tr><td>PLN</td><td>זלוטי</td></tr><tr><td>RON</td><td>לאו רומני</td></tr><tr><td>ZAR</td><td>ראנד דרא״פ</td></tr><tr><td>HRK</td><td>קונה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amount</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total amount, in requested currency (including the VAT, Discount &amp; Rounding)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document description</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="creationDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">creationDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Creation date Unix timestamp (in seconds)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="footer"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">footer</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document footer text</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="remarks"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">remarks</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document remarks</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amountLocal"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amountLocal</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total amount in local currency, including VAT, discount, and rounding</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amountOpened"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amountOpened</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The amount that is still left to be paid, exists only in payment request documents</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amountDueVat"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amountDueVat</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Amount due VAT - Amount before VAT, and before rounding &amp; discount (if requested)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amountExemptVat"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amountExemptVat</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Amount exempt VAT - 0 unless there's one or more items that are excluded of VAT such as mixed documents (that have both VAT excluded &amp; included items)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amountExcludeVat"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amountExcludeVat</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Amount excluded from VAT</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="vat"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">vat</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>VAT amount</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="vatRate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">vatRate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>VAT rate applied to the document</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currencyRate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currencyRate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Currency rate relative to ILS</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="vatType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">vatType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentVatType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document-level VAT type.</p><table><thead><tr><th>Value</th><th>Meaning</th></tr></thead><tbody><tr><td>0</td><td>Default (based on business type)</td></tr><tr><td>1</td><td>Exempt (VAT-free)</td></tr><tr><td>2</td><td>Mixed (contains both exempt and taxable rows)</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="client"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand client"><span class="property-name">client</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Client linked to the document</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="business"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand business"><span class="property-name">business</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Business that issued the document</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="data"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand data"><span class="property-name">data</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Tax Authority confirmation data</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="income"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand income"><span class="property-name">income</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (IncomeRow)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Income rows</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="payment"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand payment"><span class="property-name">payment</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentPaymentRow)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Payment rows</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="linkedDocuments"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand linkedDocuments"><span class="property-name">linkedDocuments</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (LinkedDocument)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Documents linked to this one</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="ref"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">ref</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integers</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The referred document types.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>10</td><td>הצעת מחיר</td></tr><tr><td>100</td><td>הזמנה</td></tr><tr><td>200</td><td>תעודת משלוח</td></tr><tr><td>210</td><td>תעודת החזרה</td></tr><tr><td>300</td><td>חשבון עסקה</td></tr><tr><td>305</td><td>חשבונית מס</td></tr><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>330</td><td>חשבונית זיכוי</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr><tr><td>410</td><td>ביטול תרומה</td></tr><tr><td>500</td><td>הזמנת רכש</td></tr><tr><td>600</td><td>קבלת פיקדון</td></tr><tr><td>610</td><td>משיכת פיקדון</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="signed"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">signed</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Is this document digitally signed</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="cancellable"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">cancellable</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Is this document cancellable</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="rounding"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">rounding</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether the sum was rounded or not</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="discount"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand discount"><span class="property-name">discount</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DiscountResponse)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="url"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand url"><span class="property-name">url</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document download URLs</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentUrl"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentUrl</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>URL of the hosted payment (bill) page for this document, where the client can pay it online. Returned only when the document was issued with a payment button (i.e. it has an associated payment request).</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="allocationNumber"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">allocationNumber</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Allocation Number issued by the Israeli Tax Authority</p></div></div></div></td></tr></tbody></table>

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl 'https://api.greeninvoice.co.il/api/v1/documents/57ae2ff9-0c24-43e8-b39c-a5bdcc05573d' \
  -H "Authorization: Bearer $MORNING_ACCESS_TOKEN"
```

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`{  -   "id": "57ae2ff9-0c24-43e8-b39c-a5bdcc05573d",      -   "description": "Just an order",      -   "type": 305,      -   "number": 40034,      -   "documentDate": "2026-05-12",      -   "creationDate": 1718049888,// 2024-06-10 20:04:48 UTC      -   "status": 0,      -   "lang": "he",      -   "footer": "Texts in footer",      -   "remarks": "Some remarks",      -   "amount": 354,      -   "amountLocal": 354,      -   "amountOpened": 0,      -   "amountDueVat": 300,      -   "amountExemptVat": 0,      -   "amountExcludeVat": 0,      -   "vat": 54,      -   "vatRate": 0.18,      -   "currency": "ILS",      -   "currencyRate": 1,      -   "vatType": 0,      -   "client": {          -   "id": "7944827a-c664-11e4-8231-080027271114",              -   "name": "John Doe",              -   "taxId": "0123456789",              -   "department": "Sales",              -   "address": "1 Luria St",              -   "city": "Tel Aviv",              -   "zip": "1234567",              -   "country": "IL",              -   "phone": "+972-54-1234567",              -   "fax": "+972-54-1234567",              -   "mobile": "+972-54-1234567",              -   "emails": [                  -   "email1@example.com"                               ],              -   "self": false                   },      -   "business": {          -   "type": 1,              -   "taxId": "123456789",              -   "name": "עסק לדוגמה",              -   "title": "כותרת לעסק",              -   "address": "רחוב סוקולוב 15",              -   "city": "תל אביב-יפו",              -   "zip": "6291790",              -   "phone": "054-1234567",              -   "fax": "054-1234567",              -   "mobile": "054-1234567",              -   "website": "[https://www.greeninvoice.co.il](https://www.greeninvoice.co.il)",              -   "email": "john@gmail.com",              -   "bankName": "לאומי",              -   "bankBranch": "44",              -   "bankAccount": "565656565656",              -   "bankSwift": "FIRBILIT",              -   "bankAba": "04064927",              -   "bankIban": "IL170108000000012612345",              -   "bankBeneficiary": "יעקב כהן",              -   "exemption": false                   },      -   "data": {          -   "taxAuthorityConfirmationNumber": "20241104100000000000001",              -   "taxAuthorityConfirmationInitiated": true,              -   "taxAuthorityConfirmationLastError": 0                   },      -   "income": [          -   {                  -   "catalogNum": "MXDFSDD",                      -   "description": "Item description",                      -   "quantity": 1,                      -   "price": 300,                      -   "currency": "ILS",                      -   "currencyRate": 1,                      -   "vatType": 1,                      -   "vatRate": 0.18,                      -   "amount": 300,                      -   "vat": 54,                      -   "amountTotal": 354,                      -   "itemId": "8b338c95-095e-46d4-b2c6-331747508759"                               }                   ],      -   "payment": [          -   {                  -   "name": "כרטיס אשראי",                      -   "type": 3,                      -   "subType": 1,                      -   "appType": 1,                      -   "price": 300,                      -   "currency": "ILS",                      -   "ref": [                          -   305                                           ],                      -   "cancellable": false                               }                   ],      -   "linkedDocuments": [          -   {                  -   "id": "a8804e5b-1031-4868-8332-76efb328961f",                      -   "type": 305,                      -   "number": 12323,                      -   "documentDate": "2026-05-12",                      -   "amount": 354,                      -   "currency": "ILS",                      -   "currencyRate": 1,                      -   "status": 0                               }                   ],      -   "ref": [          -   305                   ],      -   "signed": true,      -   "cancellable": false,      -   "rounding": false,      -   "discount": {          -   "amount": 10,              -   "type": "sum",              -   "total": -22                   },      -   "url": {          -   "he": "string",              -   "origin": "string",              -   "en": "string"                   },      -   "paymentUrl": "[https://pages.greeninvoice.co.il/payments/bills/3fa85f64-5717-4562-b3fc-2c963f66afa6](https://pages.greeninvoice.co.il/payments/bills/3fa85f64-5717-4562-b3fc-2c963f66afa6)",      -   "allocationNumber": "20220101163314614014050888"       }`

## Get Linked Documents

get/documents/{id}/linked

gethttps://api.greeninvoice.co.il/api/v1/documents/{id}/linkedProductionSandbox

Get information about linked / related documents to a specific document.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">57ae2ff9-0c24-43e8-b39c-a5bdcc05573d</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document ID</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Linked documents retrieved successfully

##### Response Schema: application/json

Array

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Linked document ID</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currency"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currency</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Currency)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>3-letter ISO currency code.</p><table><thead><tr><th>Code</th><th>Name</th></tr></thead><tbody><tr><td>ILS</td><td>שקל</td></tr><tr><td>USD</td><td>דולר</td></tr><tr><td>EUR</td><td>אירו</td></tr><tr><td>GBP</td><td>ליש״ט</td></tr><tr><td>JPY</td><td>יין יפני</td></tr><tr><td>CHF</td><td>פרנק שוויצרי</td></tr><tr><td>CNY</td><td>יואן סיני</td></tr><tr><td>AUD</td><td>דולר אוסטרלי</td></tr><tr><td>CAD</td><td>דולר קנדי</td></tr><tr><td>RUB</td><td>רובל</td></tr><tr><td>BRL</td><td>ריאל ברזילאי</td></tr><tr><td>HKD</td><td>דולר הונג קונגי</td></tr><tr><td>SGD</td><td>דולר סינגפורי</td></tr><tr><td>THB</td><td>באט תאילנדי</td></tr><tr><td>MXN</td><td>פזו מקסיקני</td></tr><tr><td>TRY</td><td>לירה טורקית</td></tr><tr><td>NZD</td><td>דולר ניו זילנדי</td></tr><tr><td>SEK</td><td>כתר שבדי</td></tr><tr><td>NOK</td><td>כתר נורבגי</td></tr><tr><td>DKK</td><td>כתר דני</td></tr><tr><td>KRW</td><td>וון דרום קוריאני</td></tr><tr><td>INR</td><td>רופי הודי</td></tr><tr><td>IDR</td><td>רופי אינדונזי</td></tr><tr><td>PLN</td><td>זלוטי</td></tr><tr><td>RON</td><td>לאו רומני</td></tr><tr><td>ZAR</td><td>ראנד דרא״פ</td></tr><tr><td>HRK</td><td>קונה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="type"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">type</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document type code.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>10</td><td>הצעת מחיר</td></tr><tr><td>20</td><td>חשבון / אישור תשלום</td></tr><tr><td>100</td><td>הזמנה</td></tr><tr><td>200</td><td>תעודת משלוח</td></tr><tr><td>210</td><td>תעודת החזרה</td></tr><tr><td>300</td><td>חשבון עסקה</td></tr><tr><td>305</td><td>חשבונית מס</td></tr><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>330</td><td>חשבונית זיכוי</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr><tr><td>410</td><td>ביטול תרומה</td></tr><tr><td>500</td><td>הזמנת רכש</td></tr><tr><td>600</td><td>קבלת פיקדון</td></tr><tr><td>610</td><td>משיכת פיקדון</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="number"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">number</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document serial number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="documentDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">documentDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document date in the format <code>YYYY-MM-DD</code></p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amount</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document amount</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currencyRate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currencyRate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Currency rate relative to ILS</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="status"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">status</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentStatus)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document status.</p><table><thead><tr><th>Code</th><th>Status</th></tr></thead><tbody><tr><td>0</td><td>מסמך פתוח</td></tr><tr><td>1</td><td>מסמך סגור</td></tr><tr><td>2</td><td>מסמך סומן ידנית כסגור</td></tr><tr><td>3</td><td>מסמך מבטל</td></tr><tr><td>4</td><td>מסמך שבוטל</td></tr></tbody></table></div></div></div></td></tr></tbody></table>

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl 'https://api.greeninvoice.co.il/api/v1/documents/57ae2ff9-0c24-43e8-b39c-a5bdcc05573d/linked' \
  -H "Authorization: Bearer $MORNING_ACCESS_TOKEN"
```

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`[  -   {          -   "id": "a8804e5b-1031-4868-8332-76efb328961f",              -   "type": 305,              -   "number": 12323,              -   "documentDate": "2026-05-12",              -   "amount": 354,              -   "currency": "ILS",              -   "currencyRate": 1,              -   "status": 0                   }       ]`

## Get Document Download Links

get/documents/{id}/download/links

gethttps://api.greeninvoice.co.il/api/v1/documents/{id}/download/linksProductionSandbox

Retrieve download links for a given document. The response includes the original copy plus any localised copies; the `en` link is returned only when an English copy exists.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">57ae2ff9-0c24-43e8-b39c-a5bdcc05573d</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document ID</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Download links retrieved successfully

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="he"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">he</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Copy link in Hebrew</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="en"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">en</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Copy link in English (if applicable)</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="origin"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">origin</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Original document</p></div></div></div></td></tr></tbody></table>

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl 'https://api.greeninvoice.co.il/api/v1/documents/57ae2ff9-0c24-43e8-b39c-a5bdcc05573d/download/links' \
  -H "Authorization: Bearer $MORNING_ACCESS_TOKEN"
```

### Response samples

-   200

Content type

application/json

Copy

`{  -   "he": "string",      -   "en": "string",      -   "origin": "string"       }`

## Close Document

post/documents/{id}/close

posthttps://api.greeninvoice.co.il/api/v1/documents/{id}/closeProductionSandbox

Manually close a document. The status will be set to `Manually closed`.

**Note:** Only documents currently in `Open` status can be closed via this endpoint. Attempting to close a document in any other status will return a validation error.

The response is the updated document.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">57ae2ff9-0c24-43e8-b39c-a5bdcc05573d</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document ID</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Document closed successfully

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The document unique ID</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="type"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">type</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document type code.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>10</td><td>הצעת מחיר</td></tr><tr><td>20</td><td>חשבון / אישור תשלום</td></tr><tr><td>100</td><td>הזמנה</td></tr><tr><td>200</td><td>תעודת משלוח</td></tr><tr><td>210</td><td>תעודת החזרה</td></tr><tr><td>300</td><td>חשבון עסקה</td></tr><tr><td>305</td><td>חשבונית מס</td></tr><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>330</td><td>חשבונית זיכוי</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr><tr><td>410</td><td>ביטול תרומה</td></tr><tr><td>500</td><td>הזמנת רכש</td></tr><tr><td>600</td><td>קבלת פיקדון</td></tr><tr><td>610</td><td>משיכת פיקדון</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="number"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">number</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document serial number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="documentDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">documentDate</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document reference date in the format <code>YYYY-MM-DD</code></p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="status"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">status</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentStatus)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document status.</p><table><thead><tr><th>Code</th><th>Status</th></tr></thead><tbody><tr><td>0</td><td>מסמך פתוח</td></tr><tr><td>1</td><td>מסמך סגור</td></tr><tr><td>2</td><td>מסמך סומן ידנית כסגור</td></tr><tr><td>3</td><td>מסמך מבטל</td></tr><tr><td>4</td><td>מסמך שבוטל</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="lang"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">lang</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Lang)</span></div><div><span class="sc-Nxspf lmPA-Dn">Enum:</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"he"</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"en"</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Content language</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currency"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currency</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Currency)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>3-letter ISO currency code.</p><table><thead><tr><th>Code</th><th>Name</th></tr></thead><tbody><tr><td>ILS</td><td>שקל</td></tr><tr><td>USD</td><td>דולר</td></tr><tr><td>EUR</td><td>אירו</td></tr><tr><td>GBP</td><td>ליש״ט</td></tr><tr><td>JPY</td><td>יין יפני</td></tr><tr><td>CHF</td><td>פרנק שוויצרי</td></tr><tr><td>CNY</td><td>יואן סיני</td></tr><tr><td>AUD</td><td>דולר אוסטרלי</td></tr><tr><td>CAD</td><td>דולר קנדי</td></tr><tr><td>RUB</td><td>רובל</td></tr><tr><td>BRL</td><td>ריאל ברזילאי</td></tr><tr><td>HKD</td><td>דולר הונג קונגי</td></tr><tr><td>SGD</td><td>דולר סינגפורי</td></tr><tr><td>THB</td><td>באט תאילנדי</td></tr><tr><td>MXN</td><td>פזו מקסיקני</td></tr><tr><td>TRY</td><td>לירה טורקית</td></tr><tr><td>NZD</td><td>דולר ניו זילנדי</td></tr><tr><td>SEK</td><td>כתר שבדי</td></tr><tr><td>NOK</td><td>כתר נורבגי</td></tr><tr><td>DKK</td><td>כתר דני</td></tr><tr><td>KRW</td><td>וון דרום קוריאני</td></tr><tr><td>INR</td><td>רופי הודי</td></tr><tr><td>IDR</td><td>רופי אינדונזי</td></tr><tr><td>PLN</td><td>זלוטי</td></tr><tr><td>RON</td><td>לאו רומני</td></tr><tr><td>ZAR</td><td>ראנד דרא״פ</td></tr><tr><td>HRK</td><td>קונה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amount</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total amount, in requested currency (including the VAT, Discount &amp; Rounding)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document description</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="creationDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">creationDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Creation date Unix timestamp (in seconds)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="footer"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">footer</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document footer text</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="remarks"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">remarks</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document remarks</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amountLocal"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amountLocal</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total amount in local currency, including VAT, discount, and rounding</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amountOpened"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amountOpened</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The amount that is still left to be paid, exists only in payment request documents</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amountDueVat"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amountDueVat</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Amount due VAT - Amount before VAT, and before rounding &amp; discount (if requested)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amountExemptVat"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amountExemptVat</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Amount exempt VAT - 0 unless there's one or more items that are excluded of VAT such as mixed documents (that have both VAT excluded &amp; included items)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amountExcludeVat"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amountExcludeVat</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Amount excluded from VAT</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="vat"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">vat</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>VAT amount</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="vatRate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">vatRate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>VAT rate applied to the document</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currencyRate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currencyRate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Currency rate relative to ILS</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="vatType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">vatType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentVatType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document-level VAT type.</p><table><thead><tr><th>Value</th><th>Meaning</th></tr></thead><tbody><tr><td>0</td><td>Default (based on business type)</td></tr><tr><td>1</td><td>Exempt (VAT-free)</td></tr><tr><td>2</td><td>Mixed (contains both exempt and taxable rows)</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="client"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand client"><span class="property-name">client</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Client linked to the document</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="data"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand data"><span class="property-name">data</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Tax Authority confirmation data</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="income"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand income"><span class="property-name">income</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (IncomeRow)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Income rows</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="payment"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand payment"><span class="property-name">payment</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentPaymentRow)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Payment rows</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="linkedDocuments"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand linkedDocuments"><span class="property-name">linkedDocuments</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (LinkedDocument)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Documents linked to this one</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="ref"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">ref</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integers</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The referred document types.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>10</td><td>הצעת מחיר</td></tr><tr><td>100</td><td>הזמנה</td></tr><tr><td>200</td><td>תעודת משלוח</td></tr><tr><td>210</td><td>תעודת החזרה</td></tr><tr><td>300</td><td>חשבון עסקה</td></tr><tr><td>305</td><td>חשבונית מס</td></tr><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>330</td><td>חשבונית זיכוי</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr><tr><td>410</td><td>ביטול תרומה</td></tr><tr><td>500</td><td>הזמנת רכש</td></tr><tr><td>600</td><td>קבלת פיקדון</td></tr><tr><td>610</td><td>משיכת פיקדון</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="signed"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">signed</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Is this document digitally signed</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="cancellable"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">cancellable</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Is this document cancellable</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="rounding"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">rounding</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether the sum was rounded or not</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="discount"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand discount"><span class="property-name">discount</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DiscountResponse)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="url"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand url"><span class="property-name">url</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document download URLs</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="allocationNumber"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">allocationNumber</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Allocation Number issued by the Israeli Tax Authority</p></div></div></div></td></tr></tbody></table>

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl -X POST 'https://api.greeninvoice.co.il/api/v1/documents/57ae2ff9-0c24-43e8-b39c-a5bdcc05573d/close' \
  -H "Authorization: Bearer $MORNING_ACCESS_TOKEN"
```

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`{  -   "id": "57ae2ff9-0c24-43e8-b39c-a5bdcc05573d",      -   "description": "Just an order",      -   "type": 305,      -   "number": 40034,      -   "documentDate": "2026-05-12",      -   "creationDate": 1718049888,// 2024-06-10 20:04:48 UTC      -   "status": 0,      -   "lang": "he",      -   "footer": "Texts in footer",      -   "remarks": "Some remarks",      -   "amount": 354,      -   "amountLocal": 354,      -   "amountOpened": 0,      -   "amountDueVat": 300,      -   "amountExemptVat": 0,      -   "amountExcludeVat": 0,      -   "vat": 54,      -   "vatRate": 0.18,      -   "currency": "ILS",      -   "currencyRate": 1,      -   "vatType": 0,      -   "client": {          -   "id": "7944827a-c664-11e4-8231-080027271114",              -   "name": "John Doe",              -   "taxId": "0123456789",              -   "department": "Sales",              -   "address": "1 Luria St",              -   "city": "Tel Aviv",              -   "zip": "1234567",              -   "country": "IL",              -   "phone": "+972-54-1234567",              -   "fax": "+972-54-1234567",              -   "mobile": "+972-54-1234567",              -   "emails": [                  -   "email1@example.com"                               ],              -   "self": false                   },      -   "data": {          -   "taxAuthorityConfirmationNumber": "20241104100000000000001",              -   "taxAuthorityConfirmationInitiated": true,              -   "taxAuthorityConfirmationLastError": 0                   },      -   "income": [          -   {                  -   "catalogNum": "MXDFSDD",                      -   "description": "Item description",                      -   "quantity": 1,                      -   "price": 300,                      -   "currency": "ILS",                      -   "currencyRate": 1,                      -   "vatType": 1,                      -   "vatRate": 0.18,                      -   "amount": 300,                      -   "vat": 54,                      -   "amountTotal": 354,                      -   "itemId": "8b338c95-095e-46d4-b2c6-331747508759"                               }                   ],      -   "payment": [          -   {                  -   "name": "כרטיס אשראי",                      -   "type": 3,                      -   "subType": 1,                      -   "appType": 1,                      -   "price": 300,                      -   "currency": "ILS",                      -   "ref": [                          -   305                                           ],                      -   "cancellable": false                               }                   ],      -   "linkedDocuments": [          -   {                  -   "id": "a8804e5b-1031-4868-8332-76efb328961f",                      -   "type": 305,                      -   "number": 12323,                      -   "documentDate": "2026-05-12",                      -   "amount": 354,                      -   "currency": "ILS",                      -   "currencyRate": 1,                      -   "status": 0                               }                   ],      -   "ref": [          -   305                   ],      -   "signed": true,      -   "cancellable": false,      -   "rounding": false,      -   "discount": {          -   "amount": 10,              -   "type": "sum",              -   "total": -22                   },      -   "url": {          -   "he": "string",              -   "origin": "string",              -   "en": "string"                   },      -   "allocationNumber": "20220101163314614014050888"       }`

## Open Document

post/documents/{id}/open

posthttps://api.greeninvoice.co.il/api/v1/documents/{id}/openProductionSandbox

Re-open a document that was previously manually closed. The status will be set to `Open`.

**Note:** Only documents currently in `Manually closed` status can be re-opened via this endpoint. Documents in `Closed` status (closed automatically by the system) or any other status cannot be re-opened and will return a validation error.

The response is the updated document.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">57ae2ff9-0c24-43e8-b39c-a5bdcc05573d</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document ID</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Document re-opened successfully

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The document unique ID</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="type"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">type</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document type code.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>10</td><td>הצעת מחיר</td></tr><tr><td>20</td><td>חשבון / אישור תשלום</td></tr><tr><td>100</td><td>הזמנה</td></tr><tr><td>200</td><td>תעודת משלוח</td></tr><tr><td>210</td><td>תעודת החזרה</td></tr><tr><td>300</td><td>חשבון עסקה</td></tr><tr><td>305</td><td>חשבונית מס</td></tr><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>330</td><td>חשבונית זיכוי</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr><tr><td>410</td><td>ביטול תרומה</td></tr><tr><td>500</td><td>הזמנת רכש</td></tr><tr><td>600</td><td>קבלת פיקדון</td></tr><tr><td>610</td><td>משיכת פיקדון</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="number"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">number</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document serial number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="documentDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">documentDate</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document reference date in the format <code>YYYY-MM-DD</code></p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="status"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">status</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentStatus)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document status.</p><table><thead><tr><th>Code</th><th>Status</th></tr></thead><tbody><tr><td>0</td><td>מסמך פתוח</td></tr><tr><td>1</td><td>מסמך סגור</td></tr><tr><td>2</td><td>מסמך סומן ידנית כסגור</td></tr><tr><td>3</td><td>מסמך מבטל</td></tr><tr><td>4</td><td>מסמך שבוטל</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="lang"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">lang</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Lang)</span></div><div><span class="sc-Nxspf lmPA-Dn">Enum:</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"he"</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"en"</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Content language</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currency"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currency</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Currency)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>3-letter ISO currency code.</p><table><thead><tr><th>Code</th><th>Name</th></tr></thead><tbody><tr><td>ILS</td><td>שקל</td></tr><tr><td>USD</td><td>דולר</td></tr><tr><td>EUR</td><td>אירו</td></tr><tr><td>GBP</td><td>ליש״ט</td></tr><tr><td>JPY</td><td>יין יפני</td></tr><tr><td>CHF</td><td>פרנק שוויצרי</td></tr><tr><td>CNY</td><td>יואן סיני</td></tr><tr><td>AUD</td><td>דולר אוסטרלי</td></tr><tr><td>CAD</td><td>דולר קנדי</td></tr><tr><td>RUB</td><td>רובל</td></tr><tr><td>BRL</td><td>ריאל ברזילאי</td></tr><tr><td>HKD</td><td>דולר הונג קונגי</td></tr><tr><td>SGD</td><td>דולר סינגפורי</td></tr><tr><td>THB</td><td>באט תאילנדי</td></tr><tr><td>MXN</td><td>פזו מקסיקני</td></tr><tr><td>TRY</td><td>לירה טורקית</td></tr><tr><td>NZD</td><td>דולר ניו זילנדי</td></tr><tr><td>SEK</td><td>כתר שבדי</td></tr><tr><td>NOK</td><td>כתר נורבגי</td></tr><tr><td>DKK</td><td>כתר דני</td></tr><tr><td>KRW</td><td>וון דרום קוריאני</td></tr><tr><td>INR</td><td>רופי הודי</td></tr><tr><td>IDR</td><td>רופי אינדונזי</td></tr><tr><td>PLN</td><td>זלוטי</td></tr><tr><td>RON</td><td>לאו רומני</td></tr><tr><td>ZAR</td><td>ראנד דרא״פ</td></tr><tr><td>HRK</td><td>קונה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amount</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total amount, in requested currency (including the VAT, Discount &amp; Rounding)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document description</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="creationDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">creationDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Creation date Unix timestamp (in seconds)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="footer"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">footer</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document footer text</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="remarks"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">remarks</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document remarks</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amountLocal"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amountLocal</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total amount in local currency, including VAT, discount, and rounding</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amountOpened"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amountOpened</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The amount that is still left to be paid, exists only in payment request documents</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amountDueVat"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amountDueVat</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Amount due VAT - Amount before VAT, and before rounding &amp; discount (if requested)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amountExemptVat"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amountExemptVat</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Amount exempt VAT - 0 unless there's one or more items that are excluded of VAT such as mixed documents (that have both VAT excluded &amp; included items)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amountExcludeVat"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amountExcludeVat</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Amount excluded from VAT</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="vat"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">vat</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>VAT amount</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="vatRate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">vatRate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>VAT rate applied to the document</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currencyRate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currencyRate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Currency rate relative to ILS</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="vatType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">vatType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentVatType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document-level VAT type.</p><table><thead><tr><th>Value</th><th>Meaning</th></tr></thead><tbody><tr><td>0</td><td>Default (based on business type)</td></tr><tr><td>1</td><td>Exempt (VAT-free)</td></tr><tr><td>2</td><td>Mixed (contains both exempt and taxable rows)</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="client"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand client"><span class="property-name">client</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Client linked to the document</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="data"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand data"><span class="property-name">data</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Tax Authority confirmation data</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="income"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand income"><span class="property-name">income</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (IncomeRow)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Income rows</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="payment"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand payment"><span class="property-name">payment</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentPaymentRow)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Payment rows</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="linkedDocuments"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand linkedDocuments"><span class="property-name">linkedDocuments</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (LinkedDocument)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Documents linked to this one</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="ref"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">ref</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integers</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The referred document types.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>10</td><td>הצעת מחיר</td></tr><tr><td>100</td><td>הזמנה</td></tr><tr><td>200</td><td>תעודת משלוח</td></tr><tr><td>210</td><td>תעודת החזרה</td></tr><tr><td>300</td><td>חשבון עסקה</td></tr><tr><td>305</td><td>חשבונית מס</td></tr><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>330</td><td>חשבונית זיכוי</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr><tr><td>410</td><td>ביטול תרומה</td></tr><tr><td>500</td><td>הזמנת רכש</td></tr><tr><td>600</td><td>קבלת פיקדון</td></tr><tr><td>610</td><td>משיכת פיקדון</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="signed"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">signed</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Is this document digitally signed</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="cancellable"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">cancellable</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Is this document cancellable</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="rounding"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">rounding</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether the sum was rounded or not</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="discount"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand discount"><span class="property-name">discount</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DiscountResponse)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="url"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand url"><span class="property-name">url</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document download URLs</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="allocationNumber"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">allocationNumber</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Allocation Number issued by the Israeli Tax Authority</p></div></div></div></td></tr></tbody></table>

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl -X POST 'https://api.greeninvoice.co.il/api/v1/documents/57ae2ff9-0c24-43e8-b39c-a5bdcc05573d/open' \
  -H "Authorization: Bearer $MORNING_ACCESS_TOKEN"
```

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`{  -   "id": "57ae2ff9-0c24-43e8-b39c-a5bdcc05573d",      -   "description": "Just an order",      -   "type": 305,      -   "number": 40034,      -   "documentDate": "2026-05-12",      -   "creationDate": 1718049888,// 2024-06-10 20:04:48 UTC      -   "status": 0,      -   "lang": "he",      -   "footer": "Texts in footer",      -   "remarks": "Some remarks",      -   "amount": 354,      -   "amountLocal": 354,      -   "amountOpened": 0,      -   "amountDueVat": 300,      -   "amountExemptVat": 0,      -   "amountExcludeVat": 0,      -   "vat": 54,      -   "vatRate": 0.18,      -   "currency": "ILS",      -   "currencyRate": 1,      -   "vatType": 0,      -   "client": {          -   "id": "7944827a-c664-11e4-8231-080027271114",              -   "name": "John Doe",              -   "taxId": "0123456789",              -   "department": "Sales",              -   "address": "1 Luria St",              -   "city": "Tel Aviv",              -   "zip": "1234567",              -   "country": "IL",              -   "phone": "+972-54-1234567",              -   "fax": "+972-54-1234567",              -   "mobile": "+972-54-1234567",              -   "emails": [                  -   "email1@example.com"                               ],              -   "self": false                   },      -   "data": {          -   "taxAuthorityConfirmationNumber": "20241104100000000000001",              -   "taxAuthorityConfirmationInitiated": true,              -   "taxAuthorityConfirmationLastError": 0                   },      -   "income": [          -   {                  -   "catalogNum": "MXDFSDD",                      -   "description": "Item description",                      -   "quantity": 1,                      -   "price": 300,                      -   "currency": "ILS",                      -   "currencyRate": 1,                      -   "vatType": 1,                      -   "vatRate": 0.18,                      -   "amount": 300,                      -   "vat": 54,                      -   "amountTotal": 354,                      -   "itemId": "8b338c95-095e-46d4-b2c6-331747508759"                               }                   ],      -   "payment": [          -   {                  -   "name": "כרטיס אשראי",                      -   "type": 3,                      -   "subType": 1,                      -   "appType": 1,                      -   "price": 300,                      -   "currency": "ILS",                      -   "ref": [                          -   305                                           ],                      -   "cancellable": false                               }                   ],      -   "linkedDocuments": [          -   {                  -   "id": "a8804e5b-1031-4868-8332-76efb328961f",                      -   "type": 305,                      -   "number": 12323,                      -   "documentDate": "2026-05-12",                      -   "amount": 354,                      -   "currency": "ILS",                      -   "currencyRate": 1,                      -   "status": 0                               }                   ],      -   "ref": [          -   305                   ],      -   "signed": true,      -   "cancellable": false,      -   "rounding": false,      -   "discount": {          -   "amount": 10,              -   "type": "sum",              -   "total": -22                   },      -   "url": {          -   "he": "string",              -   "origin": "string",              -   "en": "string"                   },      -   "allocationNumber": "20220101163314614014050888"       }`

## Items

While generating documents you are usually requested to add items.

Items are products that are bought from you, it can be either a real product (such as electronic device, restaurant dish) or a virtual service (such as a programmer hour).

To ease the process of entering the same item on multiple documents you are able to create an item once and use it various times later while creating a document.

## Add Item

post/items

posthttps://api.greeninvoice.co.il/api/v1/itemsProductionSandbox

Create a new catalog item for the current business.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span> <span class="sc-Nxspf sc-fxwrCY lmPA-Dn fBLaqY">&lt;= 32 characters</span></span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The item name. For example: <code>גבינייה מפוארת</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The item description. For example: <code>מאפה גבינייה אישי ומפואר</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="price"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">price</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The item price. For example: 5.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currency"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currency</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Currency)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>3-letter ISO currency code.</p><table><thead><tr><th>Code</th><th>Name</th></tr></thead><tbody><tr><td>ILS</td><td>שקל</td></tr><tr><td>USD</td><td>דולר</td></tr><tr><td>EUR</td><td>אירו</td></tr><tr><td>GBP</td><td>ליש״ט</td></tr><tr><td>JPY</td><td>יין יפני</td></tr><tr><td>CHF</td><td>פרנק שוויצרי</td></tr><tr><td>CNY</td><td>יואן סיני</td></tr><tr><td>AUD</td><td>דולר אוסטרלי</td></tr><tr><td>CAD</td><td>דולר קנדי</td></tr><tr><td>RUB</td><td>רובל</td></tr><tr><td>BRL</td><td>ריאל ברזילאי</td></tr><tr><td>HKD</td><td>דולר הונג קונגי</td></tr><tr><td>SGD</td><td>דולר סינגפורי</td></tr><tr><td>THB</td><td>באט תאילנדי</td></tr><tr><td>MXN</td><td>פזו מקסיקני</td></tr><tr><td>TRY</td><td>לירה טורקית</td></tr><tr><td>NZD</td><td>דולר ניו זילנדי</td></tr><tr><td>SEK</td><td>כתר שבדי</td></tr><tr><td>NOK</td><td>כתר נורבגי</td></tr><tr><td>DKK</td><td>כתר דני</td></tr><tr><td>KRW</td><td>וון דרום קוריאני</td></tr><tr><td>INR</td><td>רופי הודי</td></tr><tr><td>IDR</td><td>רופי אינדונזי</td></tr><tr><td>PLN</td><td>זלוטי</td></tr><tr><td>RON</td><td>לאו רומני</td></tr><tr><td>ZAR</td><td>ראנד דרא״פ</td></tr><tr><td>HRK</td><td>קונה</td></tr></tbody></table></div></div></div></td></tr></tbody></table>

### Responses

**201**

Item created successfully

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

`{  -   "name": "גבינייה מפוארת",      -   "description": "מאפה גבינייה אישי ומפואר",      -   "price": 5,      -   "currency": "ILS"       }`

### Response samples

-   201

Content type

application/json

Copy

`{  -   "id": "ff27e4fe-29d9-4f6f-b6a0-f43cdf635702",      -   "name": "גבינייה מפוארת",      -   "description": "מאפה גבינייה אישי ומפואר",      -   "price": 5,      -   "currency": "ILS",      -   "creationDate": 1780836793,// 2026-06-07 12:53:13 UTC      -   "lastUpdateDate": 1780836793// 2026-06-07 12:53:13 UTC       }`

## Get Item

get/items/{id}

gethttps://api.greeninvoice.co.il/api/v1/items/{id}ProductionSandbox

Retrieve a single item by its ID.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">ff27e4fe-29d9-4f6f-b6a0-f43cdf635702</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Item ID</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Item retrieved successfully

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The item ID</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The item name</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="price"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">price</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The item price</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currency"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currency</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Currency)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>3-letter ISO currency code.</p><table><thead><tr><th>Code</th><th>Name</th></tr></thead><tbody><tr><td>ILS</td><td>שקל</td></tr><tr><td>USD</td><td>דולר</td></tr><tr><td>EUR</td><td>אירו</td></tr><tr><td>GBP</td><td>ליש״ט</td></tr><tr><td>JPY</td><td>יין יפני</td></tr><tr><td>CHF</td><td>פרנק שוויצרי</td></tr><tr><td>CNY</td><td>יואן סיני</td></tr><tr><td>AUD</td><td>דולר אוסטרלי</td></tr><tr><td>CAD</td><td>דולר קנדי</td></tr><tr><td>RUB</td><td>רובל</td></tr><tr><td>BRL</td><td>ריאל ברזילאי</td></tr><tr><td>HKD</td><td>דולר הונג קונגי</td></tr><tr><td>SGD</td><td>דולר סינגפורי</td></tr><tr><td>THB</td><td>באט תאילנדי</td></tr><tr><td>MXN</td><td>פזו מקסיקני</td></tr><tr><td>TRY</td><td>לירה טורקית</td></tr><tr><td>NZD</td><td>דולר ניו זילנדי</td></tr><tr><td>SEK</td><td>כתר שבדי</td></tr><tr><td>NOK</td><td>כתר נורבגי</td></tr><tr><td>DKK</td><td>כתר דני</td></tr><tr><td>KRW</td><td>וון דרום קוריאני</td></tr><tr><td>INR</td><td>רופי הודי</td></tr><tr><td>IDR</td><td>רופי אינדונזי</td></tr><tr><td>PLN</td><td>זלוטי</td></tr><tr><td>RON</td><td>לאו רומני</td></tr><tr><td>ZAR</td><td>ראנד דרא״פ</td></tr><tr><td>HRK</td><td>קונה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="creationDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">creationDate</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Creation date Unix timestamp (in seconds)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="lastUpdateDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">lastUpdateDate</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Last update date Unix timestamp (in seconds)</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The item description</p></div></div></div></td></tr></tbody></table>

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl 'https://api.greeninvoice.co.il/api/v1/items/ff27e4fe-29d9-4f6f-b6a0-f43cdf635702' \
  -H "Authorization: Bearer $MORNING_ACCESS_TOKEN"
```

### Response samples

-   200

Content type

application/json

Copy

`{  -   "id": "ff27e4fe-29d9-4f6f-b6a0-f43cdf635702",      -   "name": "גבינייה מפוארת",      -   "description": "מאפה גבינייה אישי ומפואר",      -   "price": 5,      -   "currency": "ILS",      -   "creationDate": 1780836793,// 2026-06-07 12:53:13 UTC      -   "lastUpdateDate": 1780836793// 2026-06-07 12:53:13 UTC       }`

## Update Item

put/items/{id}

puthttps://api.greeninvoice.co.il/api/v1/items/{id}ProductionSandbox

Update an existing item by its ID. This is a partial update: include only the fields you want to change — any field you omit keeps its current value.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">ff27e4fe-29d9-4f6f-b6a0-f43cdf635702</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Item ID</p></div></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span> <span class="sc-Nxspf sc-fxwrCY lmPA-Dn fBLaqY">&lt;= 32 characters</span></span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The item name. For example: <code>גבינייה מפוארת</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span> <span class="sc-Nxspf sc-fxwrCY lmPA-Dn fBLaqY">&lt;= 500 characters</span></span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The item description. For example: <code>מאפה גבינה ודובדני אמרנה אישי ומפואר</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="price"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">price</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The item price. For example: 4.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currency"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currency</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Currency)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>3-letter ISO currency code.</p><table><thead><tr><th>Code</th><th>Name</th></tr></thead><tbody><tr><td>ILS</td><td>שקל</td></tr><tr><td>USD</td><td>דולר</td></tr><tr><td>EUR</td><td>אירו</td></tr><tr><td>GBP</td><td>ליש״ט</td></tr><tr><td>JPY</td><td>יין יפני</td></tr><tr><td>CHF</td><td>פרנק שוויצרי</td></tr><tr><td>CNY</td><td>יואן סיני</td></tr><tr><td>AUD</td><td>דולר אוסטרלי</td></tr><tr><td>CAD</td><td>דולר קנדי</td></tr><tr><td>RUB</td><td>רובל</td></tr><tr><td>BRL</td><td>ריאל ברזילאי</td></tr><tr><td>HKD</td><td>דולר הונג קונגי</td></tr><tr><td>SGD</td><td>דולר סינגפורי</td></tr><tr><td>THB</td><td>באט תאילנדי</td></tr><tr><td>MXN</td><td>פזו מקסיקני</td></tr><tr><td>TRY</td><td>לירה טורקית</td></tr><tr><td>NZD</td><td>דולר ניו זילנדי</td></tr><tr><td>SEK</td><td>כתר שבדי</td></tr><tr><td>NOK</td><td>כתר נורבגי</td></tr><tr><td>DKK</td><td>כתר דני</td></tr><tr><td>KRW</td><td>וון דרום קוריאני</td></tr><tr><td>INR</td><td>רופי הודי</td></tr><tr><td>IDR</td><td>רופי אינדונזי</td></tr><tr><td>PLN</td><td>זלוטי</td></tr><tr><td>RON</td><td>לאו רומני</td></tr><tr><td>ZAR</td><td>ראנד דרא״פ</td></tr><tr><td>HRK</td><td>קונה</td></tr></tbody></table></div></div></div></td></tr></tbody></table>

### Responses

**200**

Item updated successfully

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The item ID</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The item name</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="price"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">price</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The item price</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currency"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currency</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Currency)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>3-letter ISO currency code.</p><table><thead><tr><th>Code</th><th>Name</th></tr></thead><tbody><tr><td>ILS</td><td>שקל</td></tr><tr><td>USD</td><td>דולר</td></tr><tr><td>EUR</td><td>אירו</td></tr><tr><td>GBP</td><td>ליש״ט</td></tr><tr><td>JPY</td><td>יין יפני</td></tr><tr><td>CHF</td><td>פרנק שוויצרי</td></tr><tr><td>CNY</td><td>יואן סיני</td></tr><tr><td>AUD</td><td>דולר אוסטרלי</td></tr><tr><td>CAD</td><td>דולר קנדי</td></tr><tr><td>RUB</td><td>רובל</td></tr><tr><td>BRL</td><td>ריאל ברזילאי</td></tr><tr><td>HKD</td><td>דולר הונג קונגי</td></tr><tr><td>SGD</td><td>דולר סינגפורי</td></tr><tr><td>THB</td><td>באט תאילנדי</td></tr><tr><td>MXN</td><td>פזו מקסיקני</td></tr><tr><td>TRY</td><td>לירה טורקית</td></tr><tr><td>NZD</td><td>דולר ניו זילנדי</td></tr><tr><td>SEK</td><td>כתר שבדי</td></tr><tr><td>NOK</td><td>כתר נורבגי</td></tr><tr><td>DKK</td><td>כתר דני</td></tr><tr><td>KRW</td><td>וון דרום קוריאני</td></tr><tr><td>INR</td><td>רופי הודי</td></tr><tr><td>IDR</td><td>רופי אינדונזי</td></tr><tr><td>PLN</td><td>זלוטי</td></tr><tr><td>RON</td><td>לאו רומני</td></tr><tr><td>ZAR</td><td>ראנד דרא״פ</td></tr><tr><td>HRK</td><td>קונה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="creationDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">creationDate</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Creation date Unix timestamp (in seconds)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="lastUpdateDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">lastUpdateDate</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Last update date Unix timestamp (in seconds)</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The item description</p></div></div></div></td></tr></tbody></table>

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

`{  -   "name": "גבינייה מפוארת",      -   "description": "מאפה גבינה ודובדני אמרנה אישי ומפואר",      -   "price": 4,      -   "currency": "ILS"       }`

### Response samples

-   200

Content type

application/json

Copy

`{  -   "id": "ff27e4fe-29d9-4f6f-b6a0-f43cdf635702",      -   "name": "גבינייה מפוארת",      -   "description": "מאפה גבינה ודובדני אמרנה אישי ומפואר",      -   "price": 4,      -   "currency": "ILS",      -   "creationDate": 1780836793,// 2026-06-07 12:53:13 UTC      -   "lastUpdateDate": 1780839374// 2026-06-07 13:36:14 UTC       }`

## Delete Item

delete/items/{id}

deletehttps://api.greeninvoice.co.il/api/v1/items/{id}ProductionSandbox

Delete an item by its ID. The response body is an empty object.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">ff27e4fe-29d9-4f6f-b6a0-f43cdf635702</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Item ID</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Item deleted successfully

##### Response Schema: application/json

object

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl -X DELETE 'https://api.greeninvoice.co.il/api/v1/items/ff27e4fe-29d9-4f6f-b6a0-f43cdf635702' \
  -H "Authorization: Bearer $MORNING_ACCESS_TOKEN"
```

### Response samples

-   200

Content type

application/json

Copy

`{ }`

## Search Items

post/items/search

posthttps://api.greeninvoice.co.il/api/v1/items/searchProductionSandbox

Search the catalog items of the current business using any combination of the filters in the request body. All filters are optional; omitting the body returns the most recent items. Results are paginated.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### Request Body schema: application/json

optional

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="page"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">page</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><span class="sc-Nxspf lmPA-Dn">Default: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">1</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Page number to retrieve. Defaults to 1.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pageSize"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pageSize</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><span class="sc-Nxspf lmPA-Dn">Default: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">25</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Number of results per page. Defaults to 25.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by item name. For example: <code>גבינייה מפוארת</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by item description. For example: <code>מאפה גבינה</code>.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currency"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currency</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Currency)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>3-letter ISO currency code.</p><table><thead><tr><th>Code</th><th>Name</th></tr></thead><tbody><tr><td>ILS</td><td>שקל</td></tr><tr><td>USD</td><td>דולר</td></tr><tr><td>EUR</td><td>אירו</td></tr><tr><td>GBP</td><td>ליש״ט</td></tr><tr><td>JPY</td><td>יין יפני</td></tr><tr><td>CHF</td><td>פרנק שוויצרי</td></tr><tr><td>CNY</td><td>יואן סיני</td></tr><tr><td>AUD</td><td>דולר אוסטרלי</td></tr><tr><td>CAD</td><td>דולר קנדי</td></tr><tr><td>RUB</td><td>רובל</td></tr><tr><td>BRL</td><td>ריאל ברזילאי</td></tr><tr><td>HKD</td><td>דולר הונג קונגי</td></tr><tr><td>SGD</td><td>דולר סינגפורי</td></tr><tr><td>THB</td><td>באט תאילנדי</td></tr><tr><td>MXN</td><td>פזו מקסיקני</td></tr><tr><td>TRY</td><td>לירה טורקית</td></tr><tr><td>NZD</td><td>דולר ניו זילנדי</td></tr><tr><td>SEK</td><td>כתר שבדי</td></tr><tr><td>NOK</td><td>כתר נורבגי</td></tr><tr><td>DKK</td><td>כתר דני</td></tr><tr><td>KRW</td><td>וון דרום קוריאני</td></tr><tr><td>INR</td><td>רופי הודי</td></tr><tr><td>IDR</td><td>רופי אינדונזי</td></tr><tr><td>PLN</td><td>זלוטי</td></tr><tr><td>RON</td><td>לאו רומני</td></tr><tr><td>ZAR</td><td>ראנד דרא״פ</td></tr><tr><td>HRK</td><td>קונה</td></tr></tbody></table></div></div></div></td></tr></tbody></table>

### Responses

**200**

Paginated list of items matching the search

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="total"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">total</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total number of items matching the search</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="page"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">page</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The requested page number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pageSize"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pageSize</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The requested page size</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="from"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">from</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Index of the first item in the current page</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="to"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">to</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Index of the last item in the current page</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pages"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pages</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total number of pages available</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="items"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand items"><span class="property-name">items</span></button><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (SearchItem)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The items matching the search</p></div></div></div></td></tr></tbody></table>

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

`{  -   "page": 1,      -   "pageSize": 25,      -   "name": "גבינייה מפוארת",      -   "description": "מאפה גבינה",      -   "currency": "ILS"       }`

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`{  -   "total": 1,      -   "page": 1,      -   "pageSize": 25,      -   "from": 1,      -   "to": 1,      -   "pages": 1,      -   "items": [          -   {                  -   "id": "df700df9-27d2-4b03-aa8d-d65a63e37542",                      -   "name": "גבינייה מפוארת",                      -   "description": "מאפה גבינה ודובדני אמרנה אישי ומפואר",                      -   "price": 5,                      -   "currency": "ILS",                      -   "creationDate": 1780910969// 2026-06-08 09:29:29 UTC                               }                   ]       }`

## Clients

Create and manage clients — the customers you sell to and invoice.

## Add Client

post/clients

posthttps://api.greeninvoice.co.il/api/v1/clientsProductionSandbox

Create a new client for the current business.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client name. For example: <code>יעקב יעקבי</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="active"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">active</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Is the client currently active or not. Defaults to <code>true</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="send"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">send</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether to automatically send emails to the client when assigning them to a document. Defaults to <code>true</code> when the client has at least one email address.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="department"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">department</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client department. For example: <code>מחלקת כספים</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="taxId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">taxId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client tax ID. For example: <code>999152580</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="accountingKey"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">accountingKey</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client accounting key. Generated automatically if omitted. For example: <code>b6230777</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentTerms"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentTerms</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (PaymentTerm)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Payment term.</p><table><thead><tr><th>Code</th><th>Term</th></tr></thead><tbody><tr><td>-1</td><td>מיידי</td></tr><tr><td>0</td><td>שוטף</td></tr><tr><td>10</td><td>שוטף +10</td></tr><tr><td>15</td><td>שוטף +15</td></tr><tr><td>30</td><td>שוטף +30</td></tr><tr><td>45</td><td>שוטף +45</td></tr><tr><td>60</td><td>שוטף +60</td></tr><tr><td>75</td><td>שוטף +75</td></tr><tr><td>90</td><td>שוטף +90</td></tr><tr><td>120</td><td>שוטף +120</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankName"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankName</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client bank name. For example: <code>12</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankBranch"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankBranch</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client bank branch number. For example: <code>450</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankAccount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankAccount</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client bank account number. For example: <code>1111</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="address"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">address</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client address. For example: <code>הרצל 5</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="city"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">city</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client city. For example: <code>תל אביב</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="zip"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">zip</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client ZIP code. For example: <code>5555</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="country"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">country</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>2-letter ISO 3166-1 alpha-2 country code. Defaults to <code>IL</code> (Israel). Use the <a href="#operation/getSupportedCountries">Get Supported Countries</a> endpoint to retrieve the full list. For example: <code>IL</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="category"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">category</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The business category code this client is related to. Use the <a href="#operation/getSupportedBusinessCategories">Get Supported Business Categories</a> endpoint to retrieve the full list. For example: 4.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="subCategory"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">subCategory</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The business sub-category code this client is related to. Use the <a href="#operation/getSupportedBusinessCategories">Get Supported Business Categories</a> endpoint to retrieve the full list. For example: 406.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="phone"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">phone</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client phone number. For example: <code>0505555555</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="fax"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">fax</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client fax number. For example: <code>033333333</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="mobile"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">mobile</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client mobile number. For example: <code>033333333</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="remarks"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">remarks</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Client remarks for internal use. For example: <code>לקוח קבוע</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="contactPerson"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">contactPerson</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client contact person name. For example: <code>יעקב</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="emails"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">emails</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span><span> <span class="sc-Nxspf sc-fxwrCY lmPA-Dn fBLaqY">&lt;= 5 items</span></span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client email addresses (up to 5). For example: <code>["test@test-yakov.com"]</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="labels"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">labels</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span><span> <span class="sc-Nxspf sc-fxwrCY lmPA-Dn fBLaqY">&lt;= 3 items</span></span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Label IDs to assign to the client (up to 3). For example: <code>["3777a6ef-fac3-4b2e-a296-238d5dcd6450"]</code>.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="balance"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">balance</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Opening balance for the client. This value is primarily computed by the system from the client's documents and payments; provide it only to set an initial balance. For example: 0.</p></div></div></div></td></tr></tbody></table>

### Responses

**201**

Client created successfully

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

Expand all Collapse all

`{  -   "name": "יעקב יעקבי",      -   "active": true,      -   "send": true,      -   "department": "מחלקת כספים",      -   "taxId": "999152580",      -   "accountingKey": "b6230777",      -   "paymentTerms": 0,      -   "bankName": "12",      -   "bankBranch": "450",      -   "bankAccount": "1111",      -   "address": "הרצל 5",      -   "city": "תל אביב",      -   "zip": "5555",      -   "country": "IL",      -   "category": 4,      -   "subCategory": 406,      -   "phone": "0505555555",      -   "fax": "033333333",      -   "mobile": "033333333",      -   "remarks": "לקוח קבוע",      -   "contactPerson": "יעקב",      -   "emails": [          -   "test@test-yakov.com"                   ],      -   "labels": [          -   "3777a6ef-fac3-4b2e-a296-238d5dcd6450"                   ],      -   "balance": 0       }`

### Response samples

-   201

Content type

application/json

Copy

Expand all Collapse all

`{  -   "id": "42aa171f-d031-4f3f-bec4-ff60c04eeafc",      -   "name": "יעקב יעקבי",      -   "active": true,      -   "send": true,      -   "department": "מחלקת כספים",      -   "taxId": "999152580",      -   "accountingKey": "b6230777",      -   "paymentTerms": 0,      -   "bankName": "12",      -   "bankBranch": "450",      -   "bankAccount": "1111",      -   "address": "הרצל 5",      -   "city": "תל אביב",      -   "zip": "5555",      -   "country": "IL",      -   "category": 4,      -   "subCategory": 406,      -   "phone": "0505555555",      -   "fax": "033333333",      -   "mobile": "033333333",      -   "emails": [          -   "test@test-yakov.com"                   ],      -   "labels": [          -   "7bd2d410-74fe-47e1-b5a3-3e544cbe2a71"                   ],      -   "remarks": "",      -   "contactPerson": "יעקב",      -   "incomeAmount": 0,      -   "paymentAmount": 0,      -   "creationDate": 1781422213,// 2026-06-14 07:30:13 UTC      -   "lastUpdateDate": 1781422213,// 2026-06-14 07:30:13 UTC      -   "balanceAmount": 0       }`

## Get Client

get/clients/{id}

gethttps://api.greeninvoice.co.il/api/v1/clients/{id}ProductionSandbox

Retrieve a single client by its ID.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">42aa171f-d031-4f3f-bec4-ff60c04eeafc</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Client ID</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Client retrieved successfully

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client ID</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client name</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="active"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">active</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Is the client currently active or not</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="send"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">send</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether emails are automatically sent to the client when assigning them to a document. Set automatically on creation based on whether the client has any email addresses.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentTerms"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentTerms</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (PaymentTerm)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Payment term.</p><table><thead><tr><th>Code</th><th>Term</th></tr></thead><tbody><tr><td>-1</td><td>מיידי</td></tr><tr><td>0</td><td>שוטף</td></tr><tr><td>10</td><td>שוטף +10</td></tr><tr><td>15</td><td>שוטף +15</td></tr><tr><td>30</td><td>שוטף +30</td></tr><tr><td>45</td><td>שוטף +45</td></tr><tr><td>60</td><td>שוטף +60</td></tr><tr><td>75</td><td>שוטף +75</td></tr><tr><td>90</td><td>שוטף +90</td></tr><tr><td>120</td><td>שוטף +120</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="incomeAmount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">incomeAmount</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total income recorded from the client. Computed by the system.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentAmount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentAmount</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total payments received from the client. Computed by the system.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="balanceAmount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">balanceAmount</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client balance amount. Computed as paymentAmount minus incomeAmount.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="creationDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">creationDate</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Creation date Unix timestamp (in seconds)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="lastUpdateDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">lastUpdateDate</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Last update date Unix timestamp (in seconds)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="department"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">department</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client department</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="taxId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">taxId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client tax ID</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="accountingKey"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">accountingKey</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client accounting key</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankName"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankName</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client bank name</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankBranch"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankBranch</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client bank branch number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankAccount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankAccount</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client bank account number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="address"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">address</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client address</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="city"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">city</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client city</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="zip"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">zip</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client ZIP code</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="country"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">country</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>2-letter ISO 3166-1 alpha-2 country code</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="category"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">category</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The business category code this client is related to. Use the <a href="#operation/getSupportedBusinessCategories">Get Supported Business Categories</a> endpoint to retrieve the full list.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="subCategory"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">subCategory</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The business sub-category code this client is related to. Use the <a href="#operation/getSupportedBusinessCategories">Get Supported Business Categories</a> endpoint to retrieve the full list.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="phone"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">phone</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client phone number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="fax"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">fax</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client fax number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="mobile"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">mobile</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client mobile number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="emails"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">emails</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client email addresses</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="labels"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">labels</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>IDs of the labels assigned to the client</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="remarks"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">remarks</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Client remarks for internal use</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="contactPerson"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">contactPerson</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client contact person name</p></div></div></div></td></tr></tbody></table>

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl 'https://api.greeninvoice.co.il/api/v1/clients/42aa171f-d031-4f3f-bec4-ff60c04eeafc' \
  -H "Authorization: Bearer $MORNING_ACCESS_TOKEN"
```

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`{  -   "id": "42aa171f-d031-4f3f-bec4-ff60c04eeafc",      -   "name": "יעקב יעקבי",      -   "active": true,      -   "send": true,      -   "department": "מחלקת כספים",      -   "taxId": "999152580",      -   "accountingKey": "b6230777",      -   "paymentTerms": 0,      -   "bankName": "12",      -   "bankBranch": "450",      -   "bankAccount": "1111",      -   "address": "הרצל 5",      -   "city": "תל אביב",      -   "zip": "5555",      -   "country": "IL",      -   "category": 4,      -   "subCategory": 406,      -   "phone": "0505555555",      -   "fax": "033333333",      -   "mobile": "033333333",      -   "emails": [          -   "test@test-yakov.com"                   ],      -   "labels": [          -   "7bd2d410-74fe-47e1-b5a3-3e544cbe2a71"                   ],      -   "remarks": "",      -   "contactPerson": "יעקב",      -   "incomeAmount": 0,      -   "paymentAmount": 0,      -   "creationDate": 1781422213,// 2026-06-14 07:30:13 UTC      -   "lastUpdateDate": 1781422213,// 2026-06-14 07:30:13 UTC      -   "balanceAmount": 0       }`

## Update Client

put/clients/{id}

puthttps://api.greeninvoice.co.il/api/v1/clients/{id}ProductionSandbox

Update an existing client by its ID. Only the fields you send are applied.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">42aa171f-d031-4f3f-bec4-ff60c04eeafc</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Client ID</p></div></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client name. For example: <code>יעקב יעקבי</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="active"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">active</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether the client is currently active. For example: <code>true</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="send"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">send</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether emails are automatically sent to the client when assigning them to a document. For example: <code>true</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="department"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">department</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client department. For example: <code>מחלקת כספים</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="taxId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">taxId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client tax ID. For example: <code>999152580</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="accountingKey"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">accountingKey</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client accounting key. For example: <code>b6230777</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentTerms"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentTerms</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (PaymentTerm)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Payment term.</p><table><thead><tr><th>Code</th><th>Term</th></tr></thead><tbody><tr><td>-1</td><td>מיידי</td></tr><tr><td>0</td><td>שוטף</td></tr><tr><td>10</td><td>שוטף +10</td></tr><tr><td>15</td><td>שוטף +15</td></tr><tr><td>30</td><td>שוטף +30</td></tr><tr><td>45</td><td>שוטף +45</td></tr><tr><td>60</td><td>שוטף +60</td></tr><tr><td>75</td><td>שוטף +75</td></tr><tr><td>90</td><td>שוטף +90</td></tr><tr><td>120</td><td>שוטף +120</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankName"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankName</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client bank name. For example: <code>12</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankBranch"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankBranch</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client bank branch number. For example: <code>450</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankAccount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankAccount</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client bank account number. For example: <code>1111</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="address"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">address</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client address. For example: <code>הרצל 5</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="city"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">city</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client city. For example: <code>ראשון לציון</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="zip"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">zip</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client ZIP code. For example: <code>4444</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="country"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">country</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>2-letter ISO 3166-1 alpha-2 country code. Use the <a href="#operation/getSupportedCountries">Get Supported Countries</a> endpoint to retrieve the full list. For example: <code>IL</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="category"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">category</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The business category code this client is related to. Use the <a href="#operation/getSupportedBusinessCategories">Get Supported Business Categories</a> endpoint to retrieve the full list. For example: 4.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="subCategory"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">subCategory</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The business sub-category code this client is related to. Use the <a href="#operation/getSupportedBusinessCategories">Get Supported Business Categories</a> endpoint to retrieve the full list. For example: 406.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="phone"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">phone</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client phone number. For example: <code>0505555555</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="fax"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">fax</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client fax number. For example: <code>033333333</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="mobile"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">mobile</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client mobile number. For example: <code>033333333</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="remarks"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">remarks</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Client remarks for internal use. For example: <code>לקוח קבוע</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="contactPerson"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">contactPerson</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client contact person name. For example: <code>יעקב</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="emails"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">emails</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span><span> <span class="sc-Nxspf sc-fxwrCY lmPA-Dn fBLaqY">&lt;= 5 items</span></span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client email addresses (up to 5). For example: <code>["test@test-yakov.com"]</code>.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="labels"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">labels</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span><span> <span class="sc-Nxspf sc-fxwrCY lmPA-Dn fBLaqY">&lt;= 3 items</span></span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Label IDs to assign to the client (up to 3). For example: <code>["3777a6ef-fac3-4b2e-a296-238d5dcd6450"]</code>.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Client updated successfully

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client ID</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client name</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="active"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">active</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Is the client currently active or not</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="send"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">send</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether emails are automatically sent to the client when assigning them to a document. Set automatically on creation based on whether the client has any email addresses.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentTerms"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentTerms</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (PaymentTerm)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Payment term.</p><table><thead><tr><th>Code</th><th>Term</th></tr></thead><tbody><tr><td>-1</td><td>מיידי</td></tr><tr><td>0</td><td>שוטף</td></tr><tr><td>10</td><td>שוטף +10</td></tr><tr><td>15</td><td>שוטף +15</td></tr><tr><td>30</td><td>שוטף +30</td></tr><tr><td>45</td><td>שוטף +45</td></tr><tr><td>60</td><td>שוטף +60</td></tr><tr><td>75</td><td>שוטף +75</td></tr><tr><td>90</td><td>שוטף +90</td></tr><tr><td>120</td><td>שוטף +120</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="incomeAmount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">incomeAmount</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total income recorded from the client. Computed by the system.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentAmount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentAmount</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total payments received from the client. Computed by the system.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="balanceAmount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">balanceAmount</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client balance amount. Computed as paymentAmount minus incomeAmount.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="creationDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">creationDate</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Creation date Unix timestamp (in seconds)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="lastUpdateDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">lastUpdateDate</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Last update date Unix timestamp (in seconds)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="department"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">department</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client department</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="taxId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">taxId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client tax ID</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="accountingKey"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">accountingKey</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client accounting key</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankName"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankName</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client bank name</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankBranch"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankBranch</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client bank branch number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankAccount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankAccount</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client bank account number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="address"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">address</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client address</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="city"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">city</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client city</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="zip"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">zip</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client ZIP code</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="country"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">country</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>2-letter ISO 3166-1 alpha-2 country code</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="category"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">category</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The business category code this client is related to. Use the <a href="#operation/getSupportedBusinessCategories">Get Supported Business Categories</a> endpoint to retrieve the full list.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="subCategory"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">subCategory</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The business sub-category code this client is related to. Use the <a href="#operation/getSupportedBusinessCategories">Get Supported Business Categories</a> endpoint to retrieve the full list.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="phone"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">phone</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client phone number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="fax"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">fax</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client fax number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="mobile"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">mobile</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client mobile number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="emails"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">emails</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client email addresses</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="labels"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">labels</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>IDs of the labels assigned to the client</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="remarks"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">remarks</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Client remarks for internal use</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="contactPerson"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">contactPerson</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client contact person name</p></div></div></div></td></tr></tbody></table>

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

Expand all Collapse all

`{  -   "name": "יעקב יעקבי",      -   "active": true,      -   "send": true,      -   "department": "מחלקת כספים",      -   "taxId": "999152580",      -   "accountingKey": "b6230777",      -   "paymentTerms": 0,      -   "bankName": "12",      -   "bankBranch": "450",      -   "bankAccount": "1111",      -   "address": "הרצל 5",      -   "city": "ראשון לציון",      -   "zip": "4444",      -   "country": "IL",      -   "category": 4,      -   "subCategory": 406,      -   "phone": "0505555555",      -   "fax": "033333333",      -   "mobile": "033333333",      -   "remarks": "לקוח קבוע",      -   "contactPerson": "יעקב",      -   "emails": [          -   "test@test-yakov.com"                   ],      -   "labels": [          -   "3777a6ef-fac3-4b2e-a296-238d5dcd6450"                   ]       }`

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`{  -   "id": "42aa171f-d031-4f3f-bec4-ff60c04eeafc",      -   "name": "יעקב יעקבי",      -   "active": true,      -   "send": true,      -   "department": "מחלקת כספים",      -   "taxId": "999152580",      -   "accountingKey": "b6230777",      -   "paymentTerms": 0,      -   "bankName": "12",      -   "bankBranch": "450",      -   "bankAccount": "1111",      -   "address": "הרצל 5",      -   "city": "תל אביב",      -   "zip": "5555",      -   "country": "IL",      -   "category": 4,      -   "subCategory": 406,      -   "phone": "0505555555",      -   "fax": "033333333",      -   "mobile": "033333333",      -   "emails": [          -   "test@test-yakov.com"                   ],      -   "labels": [          -   "7bd2d410-74fe-47e1-b5a3-3e544cbe2a71"                   ],      -   "remarks": "",      -   "contactPerson": "יעקב",      -   "incomeAmount": 0,      -   "paymentAmount": 0,      -   "creationDate": 1781422213,// 2026-06-14 07:30:13 UTC      -   "lastUpdateDate": 1781422213,// 2026-06-14 07:30:13 UTC      -   "balanceAmount": 0       }`

## Delete Client

delete/clients/{id}

deletehttps://api.greeninvoice.co.il/api/v1/clients/{id}ProductionSandbox

Delete a client by its ID. A client can be deleted only when it is inactive and has no associated documents, no active payment tokens, and no recurring charges. The response body is empty.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">42aa171f-d031-4f3f-bec4-ff60c04eeafc</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Client ID</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Client deleted successfully

##### Response Schema: application/json

object

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl -X DELETE 'https://api.greeninvoice.co.il/api/v1/clients/42aa171f-d031-4f3f-bec4-ff60c04eeafc' \
  -H "Authorization: Bearer $MORNING_ACCESS_TOKEN"
```

### Response samples

-   200

Content type

application/json

Copy

`{ }`

## Search Clients

post/clients/search

posthttps://api.greeninvoice.co.il/api/v1/clients/searchProductionSandbox

Search the current business's clients with optional filters. Results are paginated.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by client name. For example: <code>יעקב</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="active"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">active</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by active state. When omitted, both active and inactive clients are returned. For example: <code>true</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="email"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">email</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by client email address. For example: <code>test@test-yakov.com</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="contactPerson"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">contactPerson</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by contact person name. For example: <code>יעקב</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="labels"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">labels</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by label IDs. For example: <code>["3777a6ef-fac3-4b2e-a296-238d5dcd6450"]</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="page"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">page</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Page number to retrieve (1-based). Defaults to 1.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pageSize"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pageSize</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Number of results per page. Defaults to 25.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Paginated list of clients matching the search

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="total"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">total</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total number of clients matching the search.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="page"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">page</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The page number returned.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pageSize"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pageSize</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The number of results per page.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pages"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pages</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The total number of pages available.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="from"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">from</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>1-based index of the first item on this page.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="to"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">to</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>1-based index of the last item on this page.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="items"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand items"><span class="property-name">items</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (SearchClient)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The clients matching the search.</p></div></div></div></td></tr></tbody></table>

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

Expand all Collapse all

`{  -   "name": "יעקב",      -   "active": true,      -   "email": "test@test-yakov.com",      -   "contactPerson": "יעקב",      -   "labels": [          -   "3777a6ef-fac3-4b2e-a296-238d5dcd6450"                   ],      -   "page": 1,      -   "pageSize": 25       }`

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`{  -   "total": 1,      -   "page": 1,      -   "pageSize": 25,      -   "pages": 1,      -   "from": 1,      -   "to": 1,      -   "items": [          -   {                  -   "id": "42aa171f-d031-4f3f-bec4-ff60c04eeafc",                      -   "name": "יעקב יעקבי",                      -   "active": true,                      -   "send": true,                      -   "department": "מחלקת כספים",                      -   "taxId": "999152580",                      -   "accountingKey": "b6230777",                      -   "paymentTerms": 0,                      -   "bankName": "12",                      -   "bankBranch": "450",                      -   "bankAccount": "1111",                      -   "address": "הרצל 5",                      -   "city": "ראשון לציון",                      -   "zip": "4444",                      -   "country": "IL",                      -   "phone": "0505555555",                      -   "fax": "033333333",                      -   "mobile": "033333333",                      -   "emails": [                          -   "test@test-yakov.com"                                           ],                      -   "labels": [                          -   "7bd2d410-74fe-47e1-b5a3-3e544cbe2a71"                                           ],                      -   "remarks": "",                      -   "contactPerson": "יעקב",                      -   "incomeAmount": 0,                      -   "paymentAmount": 0,                      -   "creationDate": 1781422213,// 2026-06-14 07:30:13 UTC                      -   "lastUpdateDate": 1781525122,// 2026-06-15 12:05:22 UTC                      -   "balanceAmount": 0                               }                   ]       }`

## Associate Documents to a Client

post/clients/{id}/assoc

posthttps://api.greeninvoice.co.il/api/v1/clients/{id}/assocProductionSandbox

Associate one or more existing documents with a client. Used when a document was issued to a one-time client and needs to be associated with an existing client record.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">b0077e19-977b-4389-a2e1-f84fa0527d23</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Client ID</p></div></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The ID of the client to associate the documents with. For example: <code>b0077e19-977b-4389-a2e1-f84fa0527d23</code>.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="ids"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">ids</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>IDs of the existing documents to associate with the client. For example: <code>["85d1f759-88bb-4617-b4ae-d138582370b8"]</code>.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Documents associated successfully

##### Response Schema: application/json

object

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

Expand all Collapse all

`{  -   "id": "b0077e19-977b-4389-a2e1-f84fa0527d23",      -   "ids": [          -   "85d1f759-88bb-4617-b4ae-d138582370b8"                   ]       }`

### Response samples

-   200

Content type

application/json

Copy

`{ }`

## Update Client Balance

post/clients/{id}/balance

posthttps://api.greeninvoice.co.il/api/v1/clients/{id}/balanceProductionSandbox

Update a client's balance. Recalculates the client's payment amount so that the balance equals the requested value; send `0` to reset it to zero. The response body is empty.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">42aa171f-d031-4f3f-bec4-ff60c04eeafc</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Client ID</p></div></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="balance"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">balance</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The client's new balance. The endpoint recalculates the client's payment amount so the balance equals this value. Send <code>0</code> to reset the balance. For example: 30.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Client balance updated successfully

##### Response Schema: application/json

object

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

`{  -   "balance": 30       }`

### Response samples

-   200

Content type

application/json

Copy

`{ }`

## Merge Clients

post/clients/{id}/merge

posthttps://api.greeninvoice.co.il/api/v1/clients/{id}/mergeProductionSandbox

Merge one client into another. The inactive client identified by `mergeId` (in the body) is merged into the active client identified by `id` (in the path): the inactive client's documents and balance are transferred to the active client, and the inactive client is then deleted. One of the two clients must be inactive. The response body is empty.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">42aa171f-d031-4f3f-bec4-ff60c04eeafc</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The ID of the active client to merge into (the surviving client).</p></div></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="mergeId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">mergeId</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The ID of the inactive client to merge from. Its documents and balance are transferred to the active client (the path <code>id</code>), and the inactive client is then deleted. For example: <code>ba76e441-9266-40e5-9857-f0ca646f6bc1</code>.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Clients merged successfully

##### Response Schema: application/json

object

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

`{  -   "mergeId": "ba76e441-9266-40e5-9857-f0ca646f6bc1"       }`

### Response samples

-   200

Content type

application/json

Copy

`{ }`

## Suppliers

Create and manage suppliers — the businesses and individuals you buy from.

## Add Supplier

post/suppliers

posthttps://api.greeninvoice.co.il/api/v1/suppliersProductionSandbox

Create a new supplier for the current business.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier name. For example: <code>ישראל ישראלי</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="active"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">active</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Is the supplier currently active or not. Defaults to <code>true</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="department"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">department</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier department. For example: <code>Sales</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="taxId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">taxId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier tax ID. For example: <code>999317746</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="accountingKey"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">accountingKey</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier accounting key. For example: <code>31653639</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentTerms"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentTerms</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (PaymentTerm)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Payment term.</p><table><thead><tr><th>Code</th><th>Term</th></tr></thead><tbody><tr><td>-1</td><td>מיידי</td></tr><tr><td>0</td><td>שוטף</td></tr><tr><td>10</td><td>שוטף +10</td></tr><tr><td>15</td><td>שוטף +15</td></tr><tr><td>30</td><td>שוטף +30</td></tr><tr><td>45</td><td>שוטף +45</td></tr><tr><td>60</td><td>שוטף +60</td></tr><tr><td>75</td><td>שוטף +75</td></tr><tr><td>90</td><td>שוטף +90</td></tr><tr><td>120</td><td>שוטף +120</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankName"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankName</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier bank name. For example: <code>פועלים</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankBranch"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankBranch</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier bank branch number. For example: <code>123</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankAccount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankAccount</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier bank account number. For example: <code>123456</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="address"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">address</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier address. For example: <code>הרצל 12</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="city"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">city</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier city. For example: <code>תל אביב</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="zip"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">zip</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier ZIP code. For example: <code>6688320</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="country"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">country</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>2-letter ISO 3166-1 alpha-2 country code. Defaults to <code>IL</code> (Israel). Use the <a href="#operation/getSupportedCountries">Get Supported Countries</a> endpoint to retrieve the full list. For example: <code>IL</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="phone"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">phone</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier phone number. For example: <code>0505555555</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="fax"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">fax</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier fax number. For example: <code>0504444444</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="mobile"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">mobile</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier mobile number. For example: <code>0504444444</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="remarks"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">remarks</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Supplier remarks for internal use. For example: <code>ספק קבוע</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="contactPerson"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">contactPerson</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier contact person name. For example: <code>ישראל ישראלי</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="emails"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">emails</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span><span> <span class="sc-Nxspf sc-fxwrCY lmPA-Dn fBLaqY">&lt;= 3 items</span></span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier email addresses (up to 3). For example: <code>["test_test@test.com"]</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="labels"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">labels</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span><span> <span class="sc-Nxspf sc-fxwrCY lmPA-Dn fBLaqY">&lt;= 3 items</span></span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Label names to assign to the supplier (up to 3). For example: <code>["אינסטלטורים"]</code>.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="balanceAmount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">balanceAmount</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Opening balance for the supplier. This value is primarily computed by the system from the supplier's documents and payments; provide it only to set an initial balance. For example: 0.</p></div></div></div></td></tr></tbody></table>

### Responses

**201**

Supplier created successfully

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

Expand all Collapse all

`{  -   "name": "ישראל ישראלי",      -   "active": true,      -   "department": "Sales",      -   "taxId": "999317746",      -   "accountingKey": "31653639",      -   "paymentTerms": 0,      -   "bankName": "פועלים",      -   "bankBranch": "123",      -   "bankAccount": "123456",      -   "address": "הרצל 12",      -   "city": "תל אביב",      -   "zip": "6688320",      -   "country": "IL",      -   "phone": "0505555555",      -   "fax": "0504444444",      -   "mobile": "0504444444",      -   "remarks": "ספק קבוע",      -   "contactPerson": "ישראל ישראלי",      -   "emails": [          -   "test_test@test.com"                   ],      -   "labels": [          -   "אינסטלטורים"                   ],      -   "balanceAmount": 0       }`

### Response samples

-   201

Content type

application/json

Copy

Expand all Collapse all

`{  -   "id": "32770ce2-ca0f-469f-87cf-8d92c7826e9b",      -   "name": "ישראל ישראלי",      -   "active": true,      -   "department": "",      -   "taxId": "999317746",      -   "accountingKey": "31653639",      -   "paymentTerms": 0,      -   "bankName": "פועלים",      -   "bankBranch": "123",      -   "bankAccount": "123456",      -   "address": "הרצל 12",      -   "city": "תל אביב",      -   "zip": "6688320",      -   "country": "IL",      -   "phone": "0505555555",      -   "fax": "0504444444",      -   "mobile": "0504444444",      -   "emails": [          -   "test_test@test.com"                   ],      -   "labels": [          -   "775c188f-33a1-4d39-a5f2-cf7b82dd5bd5"                   ],      -   "remarks": "",      -   "contactPerson": "ישראל ישראלי",      -   "incomeAmount": 0,      -   "paymentAmount": 0,      -   "creationDate": 1780919300,// 2026-06-08 11:48:20 UTC      -   "lastUpdateDate": 1780919300,// 2026-06-08 11:48:20 UTC      -   "balanceAmount": 0       }`

## Get Supplier

get/suppliers/{id}

gethttps://api.greeninvoice.co.il/api/v1/suppliers/{id}ProductionSandbox

Retrieve a single supplier by its ID.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">32770ce2-ca0f-469f-87cf-8d92c7826e9b</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Supplier ID</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Supplier retrieved successfully

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier ID</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier name</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="active"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">active</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Is the supplier currently active or not</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentTerms"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentTerms</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (PaymentTerm)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Payment term.</p><table><thead><tr><th>Code</th><th>Term</th></tr></thead><tbody><tr><td>-1</td><td>מיידי</td></tr><tr><td>0</td><td>שוטף</td></tr><tr><td>10</td><td>שוטף +10</td></tr><tr><td>15</td><td>שוטף +15</td></tr><tr><td>30</td><td>שוטף +30</td></tr><tr><td>45</td><td>שוטף +45</td></tr><tr><td>60</td><td>שוטף +60</td></tr><tr><td>75</td><td>שוטף +75</td></tr><tr><td>90</td><td>שוטף +90</td></tr><tr><td>120</td><td>שוטף +120</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="incomeAmount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">incomeAmount</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total income recorded from the supplier</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentAmount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentAmount</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total amount paid to the supplier so far</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="balanceAmount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">balanceAmount</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier balance amount</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="creationDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">creationDate</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Creation date Unix timestamp (in seconds)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="lastUpdateDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">lastUpdateDate</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Last update date Unix timestamp (in seconds)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="department"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">department</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier department</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="taxId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">taxId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier tax ID</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="accountingKey"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">accountingKey</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier accounting key</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankName"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankName</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier bank name</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankBranch"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankBranch</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier bank branch number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankAccount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankAccount</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier bank account number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="address"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">address</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier address</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="city"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">city</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier city</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="zip"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">zip</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier ZIP code</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="country"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">country</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>2-letter ISO 3166-1 alpha-2 country code</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="phone"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">phone</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier phone number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="fax"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">fax</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier fax number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="mobile"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">mobile</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier mobile number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="emails"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">emails</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier email addresses</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="labels"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">labels</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>IDs of the labels assigned to the supplier</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="remarks"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">remarks</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Supplier remarks for internal use</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="contactPerson"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">contactPerson</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier contact person name</p></div></div></div></td></tr></tbody></table>

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl 'https://api.greeninvoice.co.il/api/v1/suppliers/32770ce2-ca0f-469f-87cf-8d92c7826e9b' \
  -H "Authorization: Bearer $MORNING_ACCESS_TOKEN"
```

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`{  -   "id": "32770ce2-ca0f-469f-87cf-8d92c7826e9b",      -   "name": "ישראל ישראלי",      -   "active": true,      -   "department": "",      -   "taxId": "999317746",      -   "accountingKey": "31653639",      -   "paymentTerms": 0,      -   "bankName": "פועלים",      -   "bankBranch": "123",      -   "bankAccount": "123456",      -   "address": "הרצל 12",      -   "city": "תל אביב",      -   "zip": "6688320",      -   "country": "IL",      -   "phone": "0505555555",      -   "fax": "0504444444",      -   "mobile": "0504444444",      -   "emails": [          -   "test_test@test.com"                   ],      -   "labels": [          -   "775c188f-33a1-4d39-a5f2-cf7b82dd5bd5"                   ],      -   "remarks": "",      -   "contactPerson": "ישראל ישראלי",      -   "incomeAmount": 0,      -   "paymentAmount": 0,      -   "creationDate": 1780919300,// 2026-06-08 11:48:20 UTC      -   "lastUpdateDate": 1780919300,// 2026-06-08 11:48:20 UTC      -   "balanceAmount": 0       }`

## Update Supplier

put/suppliers/{id}

puthttps://api.greeninvoice.co.il/api/v1/suppliers/{id}ProductionSandbox

Update an existing supplier by its ID. This is a partial update: include only the fields you want to change — any field you omit keeps its current value.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">32770ce2-ca0f-469f-87cf-8d92c7826e9b</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Supplier ID</p></div></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier name. For example: <code>ישראל ישראלי</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="active"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">active</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Is the supplier currently active or not. For example: <code>true</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="department"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">department</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier department. For example: <code>Sales</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="taxId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">taxId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier tax ID. For example: <code>999317746</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="accountingKey"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">accountingKey</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier accounting key. For example: <code>31653639</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentTerms"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentTerms</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (PaymentTerm)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Payment term.</p><table><thead><tr><th>Code</th><th>Term</th></tr></thead><tbody><tr><td>-1</td><td>מיידי</td></tr><tr><td>0</td><td>שוטף</td></tr><tr><td>10</td><td>שוטף +10</td></tr><tr><td>15</td><td>שוטף +15</td></tr><tr><td>30</td><td>שוטף +30</td></tr><tr><td>45</td><td>שוטף +45</td></tr><tr><td>60</td><td>שוטף +60</td></tr><tr><td>75</td><td>שוטף +75</td></tr><tr><td>90</td><td>שוטף +90</td></tr><tr><td>120</td><td>שוטף +120</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankName"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankName</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier bank name. For example: <code>פועלים</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankBranch"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankBranch</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier bank branch number. For example: <code>123</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankAccount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankAccount</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier bank account number. For example: <code>123456</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="address"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">address</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier address. For example: <code>הרצל 12</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="city"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">city</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier city. For example: <code>תל אביב</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="zip"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">zip</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier ZIP code. For example: <code>6688320</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="country"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">country</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>2-letter ISO 3166-1 alpha-2 country code. Defaults to <code>IL</code> (Israel). Use the <a href="#operation/getSupportedCountries">Get Supported Countries</a> endpoint to retrieve the full list. For example: <code>IL</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="phone"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">phone</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier phone number. For example: <code>0505555555</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="fax"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">fax</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier fax number. For example: <code>0504444444</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="mobile"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">mobile</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier mobile number. For example: <code>0504444444</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="remarks"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">remarks</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Supplier remarks for internal use. For example: <code>ספק קבוע</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="contactPerson"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">contactPerson</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier contact person name. For example: <code>ישראל ישראלי</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="emails"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">emails</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span><span> <span class="sc-Nxspf sc-fxwrCY lmPA-Dn fBLaqY">&lt;= 3 items</span></span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier email addresses (up to 3). For example: <code>["test_test@test.com"]</code>.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="labels"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">labels</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span><span> <span class="sc-Nxspf sc-fxwrCY lmPA-Dn fBLaqY">&lt;= 3 items</span></span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Label names to assign to the supplier (up to 3). For example: <code>["אינסטלטורים"]</code>.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Supplier updated successfully

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier ID</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier name</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="active"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">active</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Is the supplier currently active or not</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentTerms"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentTerms</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (PaymentTerm)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Payment term.</p><table><thead><tr><th>Code</th><th>Term</th></tr></thead><tbody><tr><td>-1</td><td>מיידי</td></tr><tr><td>0</td><td>שוטף</td></tr><tr><td>10</td><td>שוטף +10</td></tr><tr><td>15</td><td>שוטף +15</td></tr><tr><td>30</td><td>שוטף +30</td></tr><tr><td>45</td><td>שוטף +45</td></tr><tr><td>60</td><td>שוטף +60</td></tr><tr><td>75</td><td>שוטף +75</td></tr><tr><td>90</td><td>שוטף +90</td></tr><tr><td>120</td><td>שוטף +120</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="incomeAmount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">incomeAmount</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total income recorded from the supplier</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentAmount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentAmount</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total amount paid to the supplier so far</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="balanceAmount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">balanceAmount</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier balance amount</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="creationDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">creationDate</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Creation date Unix timestamp (in seconds)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="lastUpdateDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">lastUpdateDate</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Last update date Unix timestamp (in seconds)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="department"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">department</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier department</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="taxId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">taxId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier tax ID</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="accountingKey"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">accountingKey</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier accounting key</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankName"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankName</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier bank name</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankBranch"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankBranch</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier bank branch number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankAccount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankAccount</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier bank account number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="address"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">address</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier address</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="city"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">city</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier city</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="zip"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">zip</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier ZIP code</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="country"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">country</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>2-letter ISO 3166-1 alpha-2 country code</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="phone"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">phone</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier phone number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="fax"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">fax</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier fax number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="mobile"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">mobile</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier mobile number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="emails"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">emails</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier email addresses</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="labels"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">labels</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>IDs of the labels assigned to the supplier</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="remarks"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">remarks</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Supplier remarks for internal use</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="contactPerson"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">contactPerson</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier contact person name</p></div></div></div></td></tr></tbody></table>

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

Expand all Collapse all

`{  -   "name": "ישראל ישראלי",      -   "active": true,      -   "department": "Sales",      -   "taxId": "999317746",      -   "accountingKey": "31653639",      -   "paymentTerms": 0,      -   "bankName": "פועלים",      -   "bankBranch": "123",      -   "bankAccount": "123456",      -   "address": "הרצל 12",      -   "city": "תל אביב",      -   "zip": "6688320",      -   "country": "IL",      -   "phone": "0505555555",      -   "fax": "0504444444",      -   "mobile": "0504444444",      -   "remarks": "ספק קבוע",      -   "contactPerson": "ישראל ישראלי",      -   "emails": [          -   "test_test@test.com"                   ],      -   "labels": [          -   "אינסטלטורים"                   ]       }`

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`{  -   "id": "32770ce2-ca0f-469f-87cf-8d92c7826e9b",      -   "name": "ישראל ישראלי",      -   "active": true,      -   "department": "",      -   "taxId": "999317746",      -   "accountingKey": "31653639",      -   "paymentTerms": -1,      -   "bankName": "פועלים",      -   "bankBranch": "123",      -   "bankAccount": "123456",      -   "address": "הרצל 13",      -   "city": "ראשון לציון",      -   "zip": "6688320",      -   "country": "IL",      -   "phone": "0505555555",      -   "fax": "0504444444",      -   "mobile": "0502222222",      -   "emails": [          -   "test_test@test.com"                   ],      -   "labels": [          -   "775c188f-33a1-4d39-a5f2-cf7b82dd5bd5"                   ],      -   "remarks": "",      -   "contactPerson": "ישראל ישראלי",      -   "incomeAmount": 0,      -   "paymentAmount": 0,      -   "creationDate": 1780919300,// 2026-06-08 11:48:20 UTC      -   "lastUpdateDate": 1780923638,// 2026-06-08 13:00:38 UTC      -   "balanceAmount": 0       }`

## Delete Supplier

delete/suppliers/{id}

deletehttps://api.greeninvoice.co.il/api/v1/suppliers/{id}ProductionSandbox

Delete a supplier by its ID. The response is the deleted supplier.

**Note:** The supplier must be **inactive** (`active: false`) before it can be deleted — deactivate it first via [Update Supplier](#operation/updateSupplier). A supplier that has linked expenses cannot be deleted.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">32770ce2-ca0f-469f-87cf-8d92c7826e9b</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Supplier ID</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Supplier deleted successfully

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier ID</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier name</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="active"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">active</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Is the supplier currently active or not</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentTerms"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentTerms</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (PaymentTerm)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Payment term.</p><table><thead><tr><th>Code</th><th>Term</th></tr></thead><tbody><tr><td>-1</td><td>מיידי</td></tr><tr><td>0</td><td>שוטף</td></tr><tr><td>10</td><td>שוטף +10</td></tr><tr><td>15</td><td>שוטף +15</td></tr><tr><td>30</td><td>שוטף +30</td></tr><tr><td>45</td><td>שוטף +45</td></tr><tr><td>60</td><td>שוטף +60</td></tr><tr><td>75</td><td>שוטף +75</td></tr><tr><td>90</td><td>שוטף +90</td></tr><tr><td>120</td><td>שוטף +120</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="incomeAmount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">incomeAmount</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total income recorded from the supplier</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentAmount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentAmount</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total amount paid to the supplier so far</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="balanceAmount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">balanceAmount</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier balance amount</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="creationDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">creationDate</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Creation date Unix timestamp (in seconds)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="lastUpdateDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">lastUpdateDate</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Last update date Unix timestamp (in seconds)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="department"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">department</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier department</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="taxId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">taxId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier tax ID</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="accountingKey"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">accountingKey</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier accounting key</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankName"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankName</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier bank name</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankBranch"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankBranch</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier bank branch number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bankAccount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bankAccount</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier bank account number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="address"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">address</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier address</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="city"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">city</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier city</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="zip"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">zip</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier ZIP code</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="country"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">country</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>2-letter ISO 3166-1 alpha-2 country code</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="phone"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">phone</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier phone number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="fax"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">fax</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier fax number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="mobile"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">mobile</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier mobile number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="emails"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">emails</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier email addresses</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="labels"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">labels</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>IDs of the labels assigned to the supplier</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="remarks"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">remarks</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Supplier remarks for internal use</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="contactPerson"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">contactPerson</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier contact person name</p></div></div></div></td></tr></tbody></table>

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl -X DELETE 'https://api.greeninvoice.co.il/api/v1/suppliers/32770ce2-ca0f-469f-87cf-8d92c7826e9b' \
  -H "Authorization: Bearer $MORNING_ACCESS_TOKEN"
```

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`{  -   "id": "32770ce2-ca0f-469f-87cf-8d92c7826e9b",      -   "name": "ישראל ישראלי",      -   "active": false,      -   "department": "",      -   "taxId": "999317746",      -   "accountingKey": "31653639",      -   "paymentTerms": -1,      -   "bankName": "פועלים",      -   "bankBranch": "123",      -   "bankAccount": "123456",      -   "address": "הרצל 13",      -   "city": "ראשון לציון",      -   "zip": "6688320",      -   "country": "IL",      -   "phone": "0505555555",      -   "fax": "0504444444",      -   "mobile": "0502222222",      -   "emails": [          -   "test_test@test.com"                   ],      -   "labels": [          -   "775c188f-33a1-4d39-a5f2-cf7b82dd5bd5"                   ],      -   "remarks": "",      -   "contactPerson": "ישראל ישראלי",      -   "incomeAmount": 0,      -   "paymentAmount": 0,      -   "creationDate": 1780919300,// 2026-06-08 11:48:20 UTC      -   "lastUpdateDate": 1780928006,// 2026-06-08 14:13:26 UTC      -   "balanceAmount": 0       }`

## Search Suppliers

post/suppliers/search

posthttps://api.greeninvoice.co.il/api/v1/suppliers/searchProductionSandbox

Search the suppliers of the current business using any combination of the filters in the request body. All filters are optional; omitting the body returns the most recent suppliers. Results are paginated.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### Request Body schema: application/json

optional

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="page"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">page</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><span class="sc-Nxspf lmPA-Dn">Default: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">1</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Page number to retrieve. Defaults to 1.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pageSize"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pageSize</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><span class="sc-Nxspf lmPA-Dn">Default: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">25</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Number of results per page. Defaults to 25.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by supplier name. For example: <code>ישראל ישראלי</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="active"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">active</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by active state. Omit to return both active and inactive suppliers. For example: <code>true</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="email"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">email</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by supplier email. For example: <code>test_test@test.com</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="contactPerson"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">contactPerson</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by supplier contact person. For example: <code>ישראל ישראלי</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="taxId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">taxId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by supplier tax ID. For example: <code>999317746</code>.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="labels"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">labels</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by label IDs. For example: <code>["775c188f-33a1-4d39-a5f2-cf7b82dd5bd5"]</code>.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Paginated list of suppliers matching the search

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="total"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">total</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total number of suppliers matching the search</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="page"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">page</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The requested page number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pageSize"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pageSize</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The requested page size</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="from"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">from</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Index of the first supplier in the current page</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="to"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">to</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Index of the last supplier in the current page</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pages"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pages</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total number of pages available</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="items"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand items"><span class="property-name">items</span></button><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Supplier)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The suppliers matching the search</p></div></div></div></td></tr></tbody></table>

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

Expand all Collapse all

`{  -   "page": 1,      -   "pageSize": 25,      -   "name": "ישראל ישראלי",      -   "active": true,      -   "email": "test_test@test.com",      -   "contactPerson": "ישראל ישראלי",      -   "taxId": "999317746",      -   "labels": [          -   "775c188f-33a1-4d39-a5f2-cf7b82dd5bd5"                   ]       }`

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`{  -   "total": 1,      -   "page": 1,      -   "pageSize": 25,      -   "from": 1,      -   "to": 1,      -   "pages": 1,      -   "items": [          -   {                  -   "id": "32770ce2-ca0f-469f-87cf-8d92c7826e9b",                      -   "name": "ישראל ישראלי",                      -   "active": true,                      -   "department": "",                      -   "taxId": "999317746",                      -   "accountingKey": "31653639",                      -   "paymentTerms": 0,                      -   "bankName": "פועלים",                      -   "bankBranch": "123",                      -   "bankAccount": "123456",                      -   "address": "הרצל 12",                      -   "city": "תל אביב",                      -   "zip": "6688320",                      -   "country": "IL",                      -   "phone": "0505555555",                      -   "fax": "0504444444",                      -   "mobile": "0504444444",                      -   "emails": [                          -   "test_test@test.com"                                           ],                      -   "labels": [                          -   "775c188f-33a1-4d39-a5f2-cf7b82dd5bd5"                                           ],                      -   "remarks": "",                      -   "contactPerson": "ישראל ישראלי",                      -   "incomeAmount": 0,                      -   "paymentAmount": 0,                      -   "creationDate": 1780919300,// 2026-06-08 11:48:20 UTC                      -   "lastUpdateDate": 1780919300,// 2026-06-08 11:48:20 UTC                      -   "balanceAmount": 0                               }                   ]       }`

## Merge Suppliers

post/suppliers/{id}/merge

posthttps://api.greeninvoice.co.il/api/v1/suppliers/{id}/mergeProductionSandbox

Merge one supplier into another. The supplier identified by the path `id` is the **target** that data is merged into; the `mergeId` in the request body is the **source** supplier that data is merged from.

**Note:** One of the two suppliers must be inactive — specifically the source (`mergeId`). After the merge the source supplier is deleted and all of its documents are reassigned to the target supplier. The response body is an empty object.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">fa12ede8-6b22-4566-abfd-5a801e6b0fb4</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The target supplier ID (the supplier that data is merged into)</p></div></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="mergeId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">mergeId</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The ID of the supplier to merge data from. Must be an inactive supplier — after the merge it is deleted and all of its documents are reassigned to the target supplier. For example: <code>6e8f79d3-ed3e-4940-ad95-94c5416e9b19</code>.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Suppliers merged successfully

##### Response Schema: application/json

object

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

`{  -   "mergeId": "6e8f79d3-ed3e-4940-ad95-94c5416e9b19"       }`

### Response samples

-   200

Content type

application/json

Copy

`{ }`

## Expenses

Track and manage your business expenses — the money your business spends on purchases and services.

You can create an expense in two ways:

-   **Without a file** — the expense is created immediately and is ready to use.
-   **With a file** (such as a receipt or invoice) — the upload first becomes an **expense draft**. Review the draft, then approve it to turn it into a regular expense.

A draft is simply a pending expense waiting for your approval; until then, it isn't counted as an actual expense.

## Add Expense

post/expenses

posthttps://api.greeninvoice.co.il/api/v1/expensesProductionSandbox

Add an expense to the current business.

The expense is generated from the business and document default settings, overridden by any attributes provided in the request.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="documentType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">documentType</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpenseDocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense document type code.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>20</td><td>חשבון / אישור תשלום</td></tr><tr><td>305</td><td>חשבונית מס</td></tr><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>330</td><td>חשבונית זיכוי</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="number"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">number</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier's document number. For example: <code>100</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="date"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">date</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Date of the expense, formatted YYYY-MM-DD. Must be 2010-01-01 or later and not in the future. For example: <code>2026-05-06</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="reportingDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">reportingDate</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>VAT reporting date. Must be the first day of the month, formatted YYYY-MM-01. For example: <code>2026-05-01</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="supplier"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand supplier"><span class="property-name">supplier</span></button><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpenseSupplierRequest)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="accountingClassification"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand accountingClassification"><span class="property-name">accountingClassification</span></button><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (AccountingClassification)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Accounting classification (expense category). On the request, send an existing classification's <code>id</code> (from the Get Accounting Classifications endpoint), or the details (<code>irsCode</code>, <code>title</code>, <code>income</code>, <code>vat</code>) to classify inline.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpensePaymentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense payment method.</p><table><thead><tr><th>Code</th><th>Method</th></tr></thead><tbody><tr><td>-1</td><td>לא שולם</td></tr><tr><td>1</td><td>מזומן</td></tr><tr><td>2</td><td>צ׳ק</td></tr><tr><td>3</td><td>כרטיס אשראי</td></tr><tr><td>4</td><td>העברה בנקאית</td></tr><tr><td>5</td><td>פייפאל</td></tr><tr><td>10</td><td>אפליקציית תשלום</td></tr><tr><td>11</td><td>אחר</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currency"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currency</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Currency)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>3-letter ISO currency code.</p><table><thead><tr><th>Code</th><th>Name</th></tr></thead><tbody><tr><td>ILS</td><td>שקל</td></tr><tr><td>USD</td><td>דולר</td></tr><tr><td>EUR</td><td>אירו</td></tr><tr><td>GBP</td><td>ליש״ט</td></tr><tr><td>JPY</td><td>יין יפני</td></tr><tr><td>CHF</td><td>פרנק שוויצרי</td></tr><tr><td>CNY</td><td>יואן סיני</td></tr><tr><td>AUD</td><td>דולר אוסטרלי</td></tr><tr><td>CAD</td><td>דולר קנדי</td></tr><tr><td>RUB</td><td>רובל</td></tr><tr><td>BRL</td><td>ריאל ברזילאי</td></tr><tr><td>HKD</td><td>דולר הונג קונגי</td></tr><tr><td>SGD</td><td>דולר סינגפורי</td></tr><tr><td>THB</td><td>באט תאילנדי</td></tr><tr><td>MXN</td><td>פזו מקסיקני</td></tr><tr><td>TRY</td><td>לירה טורקית</td></tr><tr><td>NZD</td><td>דולר ניו זילנדי</td></tr><tr><td>SEK</td><td>כתר שבדי</td></tr><tr><td>NOK</td><td>כתר נורבגי</td></tr><tr><td>DKK</td><td>כתר דני</td></tr><tr><td>KRW</td><td>וון דרום קוריאני</td></tr><tr><td>INR</td><td>רופי הודי</td></tr><tr><td>IDR</td><td>רופי אינדונזי</td></tr><tr><td>PLN</td><td>זלוטי</td></tr><tr><td>RON</td><td>לאו רומני</td></tr><tr><td>ZAR</td><td>ראנד דרא״פ</td></tr><tr><td>HRK</td><td>קונה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currencyRate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currencyRate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Exchange rate relative to ILS. Defaults to 1.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amount</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total amount of the expense, including VAT. For example: 472.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="vat"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">vat</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>VAT portion of the amount. May not exceed <code>amount</code>. For example: 72.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Description of the expense. For example: <code>אינסטלטור</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="remarks"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">remarks</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Free-text remarks. For example: <code>אינסטלטור-שולם</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="labels"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">labels</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Labels used to identify the expense. For example: <code>["דחוף"]</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="allocationNumber"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">allocationNumber</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Tax Authority Allocation Number, when applicable. For example: <code>166056573</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pcnClassification"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pcnClassification</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpensePcnClassifications)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>PCN874 input classification (for the Israeli Tax Authority PCN874 report).</p><table><thead><tr><th>Value</th><th>Meaning</th></tr></thead><tbody><tr><td>T</td><td>תשומה רגילה</td></tr><tr><td>R</td><td>רשומון יבוא</td></tr><tr><td>K</td><td>ספק קופה קטנה</td></tr><tr><td>P</td><td>ספק רשות פלסטינית</td></tr><tr><td>C</td><td>תשומה חשבונית עצמית</td></tr><tr><td>H</td><td>מסמך אחר</td></tr></tbody></table></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="active"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">active</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether the expense is active. Defaults to true.</p></div></div></div></td></tr></tbody></table>

### Responses

**201**

Expense created successfully

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

Expand all Collapse all

`{  -   "documentType": 320,      -   "number": "100",      -   "date": "2026-05-06",      -   "reportingDate": "2026-05-01",      -   "paymentType": 3,      -   "currency": "ILS",      -   "currencyRate": 1,      -   "amount": 472,      -   "vat": 72,      -   "description": "אינסטלטור",      -   "remarks": "אינסטלטור-שולם",      -   "labels": [          -   "דחוף"                   ],      -   "allocationNumber": "166056573",      -   "pcnClassification": "T",      -   "supplier": {          -   "name": "ישראל ישראלי",              -   "active": true,              -   "department": "Sales",              -   "taxId": "999317746",              -   "accountingKey": "31653639",              -   "paymentTerms": 0,              -   "bankName": "פועלים",              -   "bankBranch": "123",              -   "bankAccount": "123456",              -   "address": "הרצל 12",              -   "city": "תל אביב",              -   "zip": "6688320",              -   "country": "IL",              -   "phone": "0505555555",              -   "fax": "0504444444",              -   "mobile": "0504444444",              -   "remarks": "ספק קבוע",              -   "contactPerson": "ישראל ישראלי",              -   "emails": [                  -   "test_test@test.com"                               ],              -   "labels": [                  -   "אינסטלטורים"                               ],              -   "balanceAmount": 0,              -   "add": true                   },      -   "accountingClassification": {          -   "id": "451b3028-68b7-4d1a-bf63-9bb8be24ca9d",              -   "key": "1310",              -   "code": "1300",              -   "title": "עבודות חוץ וקבלני משנה",              -   "irsCode": 1310,              -   "type": 20,              -   "income": 100,              -   "vat": 100,              -   "mixed": 100,              -   "creationDate": 1771231523,// 2026-02-16 08:45:23 UTC              -   "lastUpdateDate": 1779287537// 2026-05-20 14:32:17 UTC                   },      -   "active": true       }`

### Response samples

-   201

Content type

application/json

Copy

Expand all Collapse all

`{  -   "id": "b22f10a6-85f3-4374-b563-e1e039d5528c",      -   "businessId": "c1e4a7b2-8d3f-4a9c-b5e6-3f4a5b6c7d8e",      -   "businessType": 1,      -   "documentType": 320,      -   "status": 10,      -   "paymentType": 3,      -   "currency": "ILS",      -   "currencyRate": 1,      -   "amount": 472,      -   "vat": 72,      -   "amountExcludeVat": 400,      -   "amountLocal": 472,      -   "deductibleAmount": 400,      -   "deductibleVat": 72,      -   "date": "2026-05-06",      -   "reportingDate": "2026-05-01",      -   "number": "100",      -   "description": "אינסטלטור",      -   "remarks": "אינסטלטור-שולם",      -   "allocationNumber": "166056573",      -   "supplier": {          -   "id": "32770ce2-ca0f-469f-87cf-8d92c7826e9b",              -   "name": "ישראל ישראלי",              -   "active": true,              -   "department": "",              -   "taxId": "999317746",              -   "accountingKey": "31653639",              -   "paymentTerms": 0,              -   "bankName": "פועלים",              -   "bankBranch": "123",              -   "bankAccount": "123456",              -   "address": "הרצל 12",              -   "city": "תל אביב",              -   "zip": "6688320",              -   "country": "IL",              -   "phone": "0505555555",              -   "fax": "0504444444",              -   "mobile": "0504444444",              -   "emails": [                  -   "test_test@test.com"                               ],              -   "labels": [                  -   "775c188f-33a1-4d39-a5f2-cf7b82dd5bd5"                               ],              -   "remarks": "",              -   "contactPerson": "ישראל ישראלי",              -   "incomeAmount": 0,              -   "paymentAmount": 0,              -   "creationDate": 1780919300,// 2026-06-08 11:48:20 UTC              -   "lastUpdateDate": 1780919300,// 2026-06-08 11:48:20 UTC              -   "balanceAmount": 0                   },      -   "accountingClassification": {          -   "id": "451b3028-68b7-4d1a-bf63-9bb8be24ca9d",              -   "key": "1310",              -   "code": "1300",              -   "title": "עבודות חוץ וקבלני משנה",              -   "irsCode": 1310,              -   "type": 20,              -   "income": 100,              -   "vat": 100,              -   "mixed": 100,              -   "creationDate": 1771231523,// 2026-02-16 08:45:23 UTC              -   "lastUpdateDate": 1779287537// 2026-05-20 14:32:17 UTC                   },      -   "url": "string",      -   "data": {          -   "labels": [                  -   "string"                               ],              -   "pcnClassification": "T",              -   "pcnTaxId": "990000002"                   },      -   "creationDate": 1780991238,// 2026-06-09 07:47:18 UTC      -   "lastUpdateDate": 1780991238// 2026-06-09 07:47:18 UTC       }`

## Search Expenses

post/expenses/search

posthttps://api.greeninvoice.co.il/api/v1/expenses/searchProductionSandbox

Search the current business's expenses with optional filters. Results are paginated.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="fromDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">fromDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Start of the reporting-date range to filter by. Filters on the expense's reporting date (the VAT reporting period), not its document date. Must be the first day of the month, formatted YYYY-MM-01. For example: <code>2025-06-01</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="toDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">toDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>End of the reporting-date range to filter by. Filters on the expense's reporting date (the VAT reporting period), not its document date. Must be the first day of the month, formatted YYYY-MM-01. For example: <code>2026-06-01</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by expense description. For example: <code>אינסטלטור</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="supplierId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">supplierId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by supplier ID. For example: <code>28fa4c1d-a29b-11e4-963c-18002725111e</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="supplierName"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">supplierName</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by supplier name. For example: <code>אינסטלטור</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="number"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">number</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by the expense (supplier document) number. For example: <code>100</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paid"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paid</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by payment state. When omitted, both paid and unpaid expenses are returned. For example: <code>true</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="minAmount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">minAmount</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Minimum expense amount. For example: 100.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="maxAmount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">maxAmount</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Maximum expense amount. For example: 5000.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="documentType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">documentType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integers</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpenseDocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by one or more expense document types. For example: <code>[320]</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integers</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpensePaymentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by one or more payment methods. For example: <code>[3]</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="status"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">status</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integers</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpenseStatus)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by one or more expense statuses. For example: <code>[10]</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="page"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">page</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Page number to retrieve (1-based). Defaults to 1.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pageSize"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pageSize</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Number of results per page. Defaults to 25.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Paginated list of expenses matching the search

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="total"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">total</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total number of expenses matching the search.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="page"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">page</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The page number returned.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pageSize"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pageSize</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The number of results per page.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pages"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pages</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total number of pages available.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="from"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">from</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>1-based index of the first item on this page.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="to"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">to</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>1-based index of the last item on this page.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="items"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand items"><span class="property-name">items</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Expense)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The expenses matching the search.</p></div></div></div></td></tr></tbody></table>

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

Expand all Collapse all

`{  -   "fromDate": "2025-06-01",      -   "toDate": "2026-06-01",      -   "description": "אינסטלטור",      -   "supplierId": "28fa4c1d-a29b-11e4-963c-18002725111e",      -   "supplierName": "אינסטלטור",      -   "number": "100",      -   "paid": true,      -   "minAmount": 100,      -   "maxAmount": 5000,      -   "documentType": [          -   320                   ],      -   "paymentType": [          -   3                   ],      -   "status": [          -   10                   ],      -   "page": 1,      -   "pageSize": 25       }`

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`{  -   "total": 3,      -   "page": 1,      -   "pageSize": 25,      -   "pages": 1,      -   "from": 1,      -   "to": 3,      -   "items": [          -   {                  -   "id": "b22f10a6-85f3-4374-b563-e1e039d5528c",                      -   "businessId": "c1e4a7b2-8d3f-4a9c-b5e6-3f4a5b6c7d8e",                      -   "businessType": 1,                      -   "documentType": 320,                      -   "status": 10,                      -   "paymentType": 3,                      -   "currency": "ILS",                      -   "currencyRate": 1,                      -   "amount": 472,                      -   "vat": 72,                      -   "amountExcludeVat": 400,                      -   "amountLocal": 472,                      -   "deductibleAmount": 400,                      -   "deductibleVat": 72,                      -   "date": "2026-05-06",                      -   "reportingDate": "2026-05-01",                      -   "number": "100",                      -   "description": "אינסטלטור",                      -   "remarks": "אינסטלטור-שולם",                      -   "allocationNumber": "166056573",                      -   "supplier": {                          -   "id": "32770ce2-ca0f-469f-87cf-8d92c7826e9b",                              -   "name": "ישראל ישראלי",                              -   "active": true,                              -   "department": "",                              -   "taxId": "999317746",                              -   "accountingKey": "31653639",                              -   "paymentTerms": 0,                              -   "bankName": "פועלים",                              -   "bankBranch": "123",                              -   "bankAccount": "123456",                              -   "address": "הרצל 12",                              -   "city": "תל אביב",                              -   "zip": "6688320",                              -   "country": "IL",                              -   "phone": "0505555555",                              -   "fax": "0504444444",                              -   "mobile": "0504444444",                              -   "emails": [                                  -   "test_test@test.com"                                                       ],                              -   "labels": [                                  -   "775c188f-33a1-4d39-a5f2-cf7b82dd5bd5"                                                       ],                              -   "remarks": "",                              -   "contactPerson": "ישראל ישראלי",                              -   "incomeAmount": 0,                              -   "paymentAmount": 0,                              -   "creationDate": 1780919300,// 2026-06-08 11:48:20 UTC                              -   "lastUpdateDate": 1780919300,// 2026-06-08 11:48:20 UTC                              -   "balanceAmount": 0                                           },                      -   "accountingClassification": {                          -   "id": "451b3028-68b7-4d1a-bf63-9bb8be24ca9d",                              -   "key": "1310",                              -   "code": "1300",                              -   "title": "עבודות חוץ וקבלני משנה",                              -   "irsCode": 1310,                              -   "type": 20,                              -   "income": 100,                              -   "vat": 100,                              -   "mixed": 100,                              -   "creationDate": 1771231523,// 2026-02-16 08:45:23 UTC                              -   "lastUpdateDate": 1779287537// 2026-05-20 14:32:17 UTC                                           },                      -   "url": "string",                      -   "data": {                          -   "labels": [                                  -   "string"                                                       ],                              -   "pcnClassification": "T",                              -   "pcnTaxId": "990000002"                                           },                      -   "creationDate": 1780991238,// 2026-06-09 07:47:18 UTC                      -   "lastUpdateDate": 1780991238// 2026-06-09 07:47:18 UTC                               }                   ]       }`

## Get Expense

get/expenses/{id}

gethttps://api.greeninvoice.co.il/api/v1/expenses/{id}ProductionSandbox

Retrieve a single expense by its ID.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">b22f10a6-85f3-4374-b563-e1e039d5528c</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense ID</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Expense retrieved successfully

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The expense ID.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="businessId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">businessId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The ID of the business the expense belongs to.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="businessType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">businessType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (BusinessType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Business type.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>1</td><td>עוסק מורשה</td></tr><tr><td>2</td><td>חברה בע״מ</td></tr><tr><td>3</td><td>עוסק פטור</td></tr><tr><td>4</td><td>עמותה</td></tr><tr><td>5</td><td>חברה לתועלת הציבור</td></tr><tr><td>6</td><td>שותפות</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="documentType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">documentType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpenseDocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense document type code.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>20</td><td>חשבון / אישור תשלום</td></tr><tr><td>305</td><td>חשבונית מס</td></tr><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>330</td><td>חשבונית זיכוי</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="status"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">status</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpenseStatus)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense status.</p><table><thead><tr><th>Code</th><th>Status</th></tr></thead><tbody><tr><td>10</td><td>הוצאה אושרה לדו״ח</td></tr><tr><td>20</td><td>הוצאה נכללת בדו״ח</td></tr><tr><td>30</td><td>הוצאה שנערכה מחדש</td></tr><tr><td>40</td><td>הוצאה אושרה ע״י מייצג</td></tr><tr><td>100</td><td>הוצאה מחוקה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpensePaymentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense payment method.</p><table><thead><tr><th>Code</th><th>Method</th></tr></thead><tbody><tr><td>-1</td><td>לא שולם</td></tr><tr><td>1</td><td>מזומן</td></tr><tr><td>2</td><td>צ׳ק</td></tr><tr><td>3</td><td>כרטיס אשראי</td></tr><tr><td>4</td><td>העברה בנקאית</td></tr><tr><td>5</td><td>פייפאל</td></tr><tr><td>10</td><td>אפליקציית תשלום</td></tr><tr><td>11</td><td>אחר</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currency"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currency</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Currency)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>3-letter ISO currency code.</p><table><thead><tr><th>Code</th><th>Name</th></tr></thead><tbody><tr><td>ILS</td><td>שקל</td></tr><tr><td>USD</td><td>דולר</td></tr><tr><td>EUR</td><td>אירו</td></tr><tr><td>GBP</td><td>ליש״ט</td></tr><tr><td>JPY</td><td>יין יפני</td></tr><tr><td>CHF</td><td>פרנק שוויצרי</td></tr><tr><td>CNY</td><td>יואן סיני</td></tr><tr><td>AUD</td><td>דולר אוסטרלי</td></tr><tr><td>CAD</td><td>דולר קנדי</td></tr><tr><td>RUB</td><td>רובל</td></tr><tr><td>BRL</td><td>ריאל ברזילאי</td></tr><tr><td>HKD</td><td>דולר הונג קונגי</td></tr><tr><td>SGD</td><td>דולר סינגפורי</td></tr><tr><td>THB</td><td>באט תאילנדי</td></tr><tr><td>MXN</td><td>פזו מקסיקני</td></tr><tr><td>TRY</td><td>לירה טורקית</td></tr><tr><td>NZD</td><td>דולר ניו זילנדי</td></tr><tr><td>SEK</td><td>כתר שבדי</td></tr><tr><td>NOK</td><td>כתר נורבגי</td></tr><tr><td>DKK</td><td>כתר דני</td></tr><tr><td>KRW</td><td>וון דרום קוריאני</td></tr><tr><td>INR</td><td>רופי הודי</td></tr><tr><td>IDR</td><td>רופי אינדונזי</td></tr><tr><td>PLN</td><td>זלוטי</td></tr><tr><td>RON</td><td>לאו רומני</td></tr><tr><td>ZAR</td><td>ראנד דרא״פ</td></tr><tr><td>HRK</td><td>קונה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currencyRate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currencyRate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Exchange rate relative to ILS.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amount</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total amount of the expense, including VAT.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="vat"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">vat</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>VAT portion of the amount.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amountExcludeVat"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amountExcludeVat</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Amount excluding VAT (<code>amount</code> minus <code>vat</code>).</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amountLocal"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amountLocal</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total amount converted to local currency (ILS).</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="deductibleAmount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">deductibleAmount</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Tax-deductible amount, in local currency (ILS).</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="deductibleVat"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">deductibleVat</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Recoverable (input) VAT, in local currency (ILS).</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="date"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">date</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Date of the expense, formatted YYYY-MM-DD.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="reportingDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">reportingDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>VAT reporting date. Always the first day of the month, formatted YYYY-MM-01. For example: <code>2026-05-01</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="number"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">number</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier's document number.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Description of the expense.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="remarks"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">remarks</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Free-text remarks.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="allocationNumber"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">allocationNumber</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Tax Authority Allocation Number, when applicable. For example: <code>166056573</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="supplier"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand supplier"><span class="property-name">supplier</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Supplier)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="accountingClassification"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand accountingClassification"><span class="property-name">accountingClassification</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (AccountingClassification)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Accounting classification (expense category). On the request, send an existing classification's <code>id</code> (from the Get Accounting Classifications endpoint), or the details (<code>irsCode</code>, <code>title</code>, <code>income</code>, <code>vat</code>) to classify inline.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="url"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">url</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Download URL for the attached file. Present only when the expense has an attached file.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="data"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand data"><span class="property-name">data</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Additional expense details.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="creationDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">creationDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Creation date, as a Unix timestamp in seconds.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="lastUpdateDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">lastUpdateDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Last update date, as a Unix timestamp in seconds.</p></div></div></div></td></tr></tbody></table>

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl 'https://api.greeninvoice.co.il/api/v1/expenses/b22f10a6-85f3-4374-b563-e1e039d5528c' \
  -H "Authorization: Bearer $MORNING_ACCESS_TOKEN"
```

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`{  -   "id": "b22f10a6-85f3-4374-b563-e1e039d5528c",      -   "businessId": "c1e4a7b2-8d3f-4a9c-b5e6-3f4a5b6c7d8e",      -   "businessType": 1,      -   "documentType": 320,      -   "status": 10,      -   "paymentType": 3,      -   "currency": "ILS",      -   "currencyRate": 1,      -   "amount": 472,      -   "vat": 72,      -   "amountExcludeVat": 400,      -   "amountLocal": 472,      -   "deductibleAmount": 400,      -   "deductibleVat": 72,      -   "date": "2026-05-06",      -   "reportingDate": "2026-05-01",      -   "number": "100",      -   "description": "אינסטלטור",      -   "remarks": "אינסטלטור-שולם",      -   "allocationNumber": "166056573",      -   "supplier": {          -   "id": "32770ce2-ca0f-469f-87cf-8d92c7826e9b",              -   "name": "ישראל ישראלי",              -   "active": true,              -   "department": "",              -   "taxId": "999317746",              -   "accountingKey": "31653639",              -   "paymentTerms": 0,              -   "bankName": "פועלים",              -   "bankBranch": "123",              -   "bankAccount": "123456",              -   "address": "הרצל 12",              -   "city": "תל אביב",              -   "zip": "6688320",              -   "country": "IL",              -   "phone": "0505555555",              -   "fax": "0504444444",              -   "mobile": "0504444444",              -   "emails": [                  -   "test_test@test.com"                               ],              -   "labels": [                  -   "775c188f-33a1-4d39-a5f2-cf7b82dd5bd5"                               ],              -   "remarks": "",              -   "contactPerson": "ישראל ישראלי",              -   "incomeAmount": 0,              -   "paymentAmount": 0,              -   "creationDate": 1780919300,// 2026-06-08 11:48:20 UTC              -   "lastUpdateDate": 1780919300,// 2026-06-08 11:48:20 UTC              -   "balanceAmount": 0                   },      -   "accountingClassification": {          -   "id": "451b3028-68b7-4d1a-bf63-9bb8be24ca9d",              -   "key": "1310",              -   "code": "1300",              -   "title": "עבודות חוץ וקבלני משנה",              -   "irsCode": 1310,              -   "type": 20,              -   "income": 100,              -   "vat": 100,              -   "mixed": 100,              -   "creationDate": 1771231523,// 2026-02-16 08:45:23 UTC              -   "lastUpdateDate": 1779287537// 2026-05-20 14:32:17 UTC                   },      -   "url": "string",      -   "data": {          -   "labels": [                  -   "string"                               ],              -   "pcnClassification": "T",              -   "pcnTaxId": "990000002"                   },      -   "creationDate": 1780991238,// 2026-06-09 07:47:18 UTC      -   "lastUpdateDate": 1780991238// 2026-06-09 07:47:18 UTC       }`

## Update Expense

put/expenses/{id}

puthttps://api.greeninvoice.co.il/api/v1/expenses/{id}ProductionSandbox

Update an existing expense by its ID. Only the fields you send are applied.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">206e85f0-1606-4310-86d8-3a6736a41158</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense ID</p></div></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="documentType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">documentType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpenseDocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense document type code.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>20</td><td>חשבון / אישור תשלום</td></tr><tr><td>305</td><td>חשבונית מס</td></tr><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>330</td><td>חשבונית זיכוי</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="number"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">number</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier's document number. For example: <code>111</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="date"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">date</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Date of the expense, formatted YYYY-MM-DD. Must be 2010-01-01 or later and not in the future. For example: <code>2026-06-09</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="reportingDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">reportingDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>VAT reporting date. Must be the first day of the month, formatted YYYY-MM-01. For example: <code>2026-06-01</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpensePaymentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense payment method.</p><table><thead><tr><th>Code</th><th>Method</th></tr></thead><tbody><tr><td>-1</td><td>לא שולם</td></tr><tr><td>1</td><td>מזומן</td></tr><tr><td>2</td><td>צ׳ק</td></tr><tr><td>3</td><td>כרטיס אשראי</td></tr><tr><td>4</td><td>העברה בנקאית</td></tr><tr><td>5</td><td>פייפאל</td></tr><tr><td>10</td><td>אפליקציית תשלום</td></tr><tr><td>11</td><td>אחר</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currency"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currency</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Currency)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>3-letter ISO currency code.</p><table><thead><tr><th>Code</th><th>Name</th></tr></thead><tbody><tr><td>ILS</td><td>שקל</td></tr><tr><td>USD</td><td>דולר</td></tr><tr><td>EUR</td><td>אירו</td></tr><tr><td>GBP</td><td>ליש״ט</td></tr><tr><td>JPY</td><td>יין יפני</td></tr><tr><td>CHF</td><td>פרנק שוויצרי</td></tr><tr><td>CNY</td><td>יואן סיני</td></tr><tr><td>AUD</td><td>דולר אוסטרלי</td></tr><tr><td>CAD</td><td>דולר קנדי</td></tr><tr><td>RUB</td><td>רובל</td></tr><tr><td>BRL</td><td>ריאל ברזילאי</td></tr><tr><td>HKD</td><td>דולר הונג קונגי</td></tr><tr><td>SGD</td><td>דולר סינגפורי</td></tr><tr><td>THB</td><td>באט תאילנדי</td></tr><tr><td>MXN</td><td>פזו מקסיקני</td></tr><tr><td>TRY</td><td>לירה טורקית</td></tr><tr><td>NZD</td><td>דולר ניו זילנדי</td></tr><tr><td>SEK</td><td>כתר שבדי</td></tr><tr><td>NOK</td><td>כתר נורבגי</td></tr><tr><td>DKK</td><td>כתר דני</td></tr><tr><td>KRW</td><td>וון דרום קוריאני</td></tr><tr><td>INR</td><td>רופי הודי</td></tr><tr><td>IDR</td><td>רופי אינדונזי</td></tr><tr><td>PLN</td><td>זלוטי</td></tr><tr><td>RON</td><td>לאו רומני</td></tr><tr><td>ZAR</td><td>ראנד דרא״פ</td></tr><tr><td>HRK</td><td>קונה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currencyRate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currencyRate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Exchange rate relative to ILS. For example: 1.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amount</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total amount of the expense, including VAT. For example: 2360.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="vat"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">vat</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>VAT portion of the amount. May not exceed <code>amount</code>. For example: 360.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Description of the expense. For example: <code>מאתר נזילות</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="remarks"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">remarks</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Free-text remarks. For example: <code>מאתר נזילות - שולם</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="labels"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">labels</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Labels used to identify the expense. For example: <code>["דחוף"]</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="allocationNumber"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">allocationNumber</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Tax Authority Allocation Number, when applicable. For example: <code>166056573</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pcnClassification"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pcnClassification</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpensePcnClassifications)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>PCN874 input classification (for the Israeli Tax Authority PCN874 report).</p><table><thead><tr><th>Value</th><th>Meaning</th></tr></thead><tbody><tr><td>T</td><td>תשומה רגילה</td></tr><tr><td>R</td><td>רשומון יבוא</td></tr><tr><td>K</td><td>ספק קופה קטנה</td></tr><tr><td>P</td><td>ספק רשות פלסטינית</td></tr><tr><td>C</td><td>תשומה חשבונית עצמית</td></tr><tr><td>H</td><td>מסמך אחר</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="supplier"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand supplier"><span class="property-name">supplier</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpenseSupplierRequest)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="accountingClassification"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand accountingClassification"><span class="property-name">accountingClassification</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (AccountingClassification)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Accounting classification (expense category). On the request, send an existing classification's <code>id</code> (from the Get Accounting Classifications endpoint), or the details (<code>irsCode</code>, <code>title</code>, <code>income</code>, <code>vat</code>) to classify inline.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="active"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">active</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether the expense is active. For example: <code>true</code>.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Expense updated successfully

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The expense ID.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="businessId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">businessId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The ID of the business the expense belongs to.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="businessType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">businessType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (BusinessType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Business type.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>1</td><td>עוסק מורשה</td></tr><tr><td>2</td><td>חברה בע״מ</td></tr><tr><td>3</td><td>עוסק פטור</td></tr><tr><td>4</td><td>עמותה</td></tr><tr><td>5</td><td>חברה לתועלת הציבור</td></tr><tr><td>6</td><td>שותפות</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="documentType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">documentType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpenseDocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense document type code.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>20</td><td>חשבון / אישור תשלום</td></tr><tr><td>305</td><td>חשבונית מס</td></tr><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>330</td><td>חשבונית זיכוי</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="status"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">status</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpenseStatus)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense status.</p><table><thead><tr><th>Code</th><th>Status</th></tr></thead><tbody><tr><td>10</td><td>הוצאה אושרה לדו״ח</td></tr><tr><td>20</td><td>הוצאה נכללת בדו״ח</td></tr><tr><td>30</td><td>הוצאה שנערכה מחדש</td></tr><tr><td>40</td><td>הוצאה אושרה ע״י מייצג</td></tr><tr><td>100</td><td>הוצאה מחוקה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpensePaymentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense payment method.</p><table><thead><tr><th>Code</th><th>Method</th></tr></thead><tbody><tr><td>-1</td><td>לא שולם</td></tr><tr><td>1</td><td>מזומן</td></tr><tr><td>2</td><td>צ׳ק</td></tr><tr><td>3</td><td>כרטיס אשראי</td></tr><tr><td>4</td><td>העברה בנקאית</td></tr><tr><td>5</td><td>פייפאל</td></tr><tr><td>10</td><td>אפליקציית תשלום</td></tr><tr><td>11</td><td>אחר</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currency"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currency</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Currency)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>3-letter ISO currency code.</p><table><thead><tr><th>Code</th><th>Name</th></tr></thead><tbody><tr><td>ILS</td><td>שקל</td></tr><tr><td>USD</td><td>דולר</td></tr><tr><td>EUR</td><td>אירו</td></tr><tr><td>GBP</td><td>ליש״ט</td></tr><tr><td>JPY</td><td>יין יפני</td></tr><tr><td>CHF</td><td>פרנק שוויצרי</td></tr><tr><td>CNY</td><td>יואן סיני</td></tr><tr><td>AUD</td><td>דולר אוסטרלי</td></tr><tr><td>CAD</td><td>דולר קנדי</td></tr><tr><td>RUB</td><td>רובל</td></tr><tr><td>BRL</td><td>ריאל ברזילאי</td></tr><tr><td>HKD</td><td>דולר הונג קונגי</td></tr><tr><td>SGD</td><td>דולר סינגפורי</td></tr><tr><td>THB</td><td>באט תאילנדי</td></tr><tr><td>MXN</td><td>פזו מקסיקני</td></tr><tr><td>TRY</td><td>לירה טורקית</td></tr><tr><td>NZD</td><td>דולר ניו זילנדי</td></tr><tr><td>SEK</td><td>כתר שבדי</td></tr><tr><td>NOK</td><td>כתר נורבגי</td></tr><tr><td>DKK</td><td>כתר דני</td></tr><tr><td>KRW</td><td>וון דרום קוריאני</td></tr><tr><td>INR</td><td>רופי הודי</td></tr><tr><td>IDR</td><td>רופי אינדונזי</td></tr><tr><td>PLN</td><td>זלוטי</td></tr><tr><td>RON</td><td>לאו רומני</td></tr><tr><td>ZAR</td><td>ראנד דרא״פ</td></tr><tr><td>HRK</td><td>קונה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currencyRate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currencyRate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Exchange rate relative to ILS.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amount</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total amount of the expense, including VAT.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="vat"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">vat</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>VAT portion of the amount.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amountExcludeVat"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amountExcludeVat</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Amount excluding VAT (<code>amount</code> minus <code>vat</code>).</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amountLocal"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amountLocal</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total amount converted to local currency (ILS).</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="deductibleAmount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">deductibleAmount</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Tax-deductible amount, in local currency (ILS).</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="deductibleVat"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">deductibleVat</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Recoverable (input) VAT, in local currency (ILS).</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="date"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">date</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Date of the expense, formatted YYYY-MM-DD.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="reportingDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">reportingDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>VAT reporting date. Always the first day of the month, formatted YYYY-MM-01. For example: <code>2026-05-01</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="number"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">number</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier's document number.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Description of the expense.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="remarks"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">remarks</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Free-text remarks.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="allocationNumber"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">allocationNumber</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Tax Authority Allocation Number, when applicable. For example: <code>166056573</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="supplier"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand supplier"><span class="property-name">supplier</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Supplier)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="accountingClassification"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand accountingClassification"><span class="property-name">accountingClassification</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (AccountingClassification)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Accounting classification (expense category). On the request, send an existing classification's <code>id</code> (from the Get Accounting Classifications endpoint), or the details (<code>irsCode</code>, <code>title</code>, <code>income</code>, <code>vat</code>) to classify inline.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="url"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">url</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Download URL for the attached file. Present only when the expense has an attached file.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="data"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand data"><span class="property-name">data</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Additional expense details.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="creationDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">creationDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Creation date, as a Unix timestamp in seconds.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="lastUpdateDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">lastUpdateDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Last update date, as a Unix timestamp in seconds.</p></div></div></div></td></tr></tbody></table>

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

Expand all Collapse all

`{  -   "documentType": 320,      -   "number": "111",      -   "date": "2026-06-09",      -   "reportingDate": "2026-06-01",      -   "paymentType": 3,      -   "currency": "ILS",      -   "currencyRate": 1,      -   "amount": 2360,      -   "vat": 360,      -   "description": "מאתר נזילות",      -   "remarks": "מאתר נזילות - שולם",      -   "labels": [          -   "דחוף"                   ],      -   "allocationNumber": "166056573",      -   "pcnClassification": "T",      -   "supplier": {          -   "name": "ישראל ישראלי",              -   "active": true,              -   "department": "Sales",              -   "taxId": "999317746",              -   "accountingKey": "31653639",              -   "paymentTerms": 0,              -   "bankName": "פועלים",              -   "bankBranch": "123",              -   "bankAccount": "123456",              -   "address": "הרצל 12",              -   "city": "תל אביב",              -   "zip": "6688320",              -   "country": "IL",              -   "phone": "0505555555",              -   "fax": "0504444444",              -   "mobile": "0504444444",              -   "remarks": "ספק קבוע",              -   "contactPerson": "ישראל ישראלי",              -   "emails": [                  -   "test_test@test.com"                               ],              -   "labels": [                  -   "אינסטלטורים"                               ],              -   "balanceAmount": 0,              -   "add": true                   },      -   "accountingClassification": {          -   "id": "451b3028-68b7-4d1a-bf63-9bb8be24ca9d",              -   "key": "1310",              -   "code": "1300",              -   "title": "עבודות חוץ וקבלני משנה",              -   "irsCode": 1310,              -   "type": 20,              -   "income": 100,              -   "vat": 100,              -   "mixed": 100,              -   "creationDate": 1771231523,// 2026-02-16 08:45:23 UTC              -   "lastUpdateDate": 1779287537// 2026-05-20 14:32:17 UTC                   },      -   "active": true       }`

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`{  -   "id": "b22f10a6-85f3-4374-b563-e1e039d5528c",      -   "businessId": "c1e4a7b2-8d3f-4a9c-b5e6-3f4a5b6c7d8e",      -   "businessType": 1,      -   "documentType": 320,      -   "status": 10,      -   "paymentType": 3,      -   "currency": "ILS",      -   "currencyRate": 1,      -   "amount": 472,      -   "vat": 72,      -   "amountExcludeVat": 400,      -   "amountLocal": 472,      -   "deductibleAmount": 400,      -   "deductibleVat": 72,      -   "date": "2026-05-06",      -   "reportingDate": "2026-05-01",      -   "number": "100",      -   "description": "אינסטלטור",      -   "remarks": "אינסטלטור-שולם",      -   "allocationNumber": "166056573",      -   "supplier": {          -   "id": "32770ce2-ca0f-469f-87cf-8d92c7826e9b",              -   "name": "ישראל ישראלי",              -   "active": true,              -   "department": "",              -   "taxId": "999317746",              -   "accountingKey": "31653639",              -   "paymentTerms": 0,              -   "bankName": "פועלים",              -   "bankBranch": "123",              -   "bankAccount": "123456",              -   "address": "הרצל 12",              -   "city": "תל אביב",              -   "zip": "6688320",              -   "country": "IL",              -   "phone": "0505555555",              -   "fax": "0504444444",              -   "mobile": "0504444444",              -   "emails": [                  -   "test_test@test.com"                               ],              -   "labels": [                  -   "775c188f-33a1-4d39-a5f2-cf7b82dd5bd5"                               ],              -   "remarks": "",              -   "contactPerson": "ישראל ישראלי",              -   "incomeAmount": 0,              -   "paymentAmount": 0,              -   "creationDate": 1780919300,// 2026-06-08 11:48:20 UTC              -   "lastUpdateDate": 1780919300,// 2026-06-08 11:48:20 UTC              -   "balanceAmount": 0                   },      -   "accountingClassification": {          -   "id": "451b3028-68b7-4d1a-bf63-9bb8be24ca9d",              -   "key": "1310",              -   "code": "1300",              -   "title": "עבודות חוץ וקבלני משנה",              -   "irsCode": 1310,              -   "type": 20,              -   "income": 100,              -   "vat": 100,              -   "mixed": 100,              -   "creationDate": 1771231523,// 2026-02-16 08:45:23 UTC              -   "lastUpdateDate": 1779287537// 2026-05-20 14:32:17 UTC                   },      -   "url": "string",      -   "data": {          -   "labels": [                  -   "string"                               ],              -   "pcnClassification": "T",              -   "pcnTaxId": "990000002"                   },      -   "creationDate": 1780991238,// 2026-06-09 07:47:18 UTC      -   "lastUpdateDate": 1780991238// 2026-06-09 07:47:18 UTC       }`

## Delete Expense

delete/expenses/{id}

deletehttps://api.greeninvoice.co.il/api/v1/expenses/{id}ProductionSandbox

Delete an expense by its ID. Returns the deleted expense.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">b22f10a6-85f3-4374-b563-e1e039d5528c</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense ID</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Expense deleted successfully

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The expense ID.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="businessId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">businessId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The ID of the business the expense belongs to.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="businessType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">businessType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (BusinessType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Business type.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>1</td><td>עוסק מורשה</td></tr><tr><td>2</td><td>חברה בע״מ</td></tr><tr><td>3</td><td>עוסק פטור</td></tr><tr><td>4</td><td>עמותה</td></tr><tr><td>5</td><td>חברה לתועלת הציבור</td></tr><tr><td>6</td><td>שותפות</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="documentType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">documentType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpenseDocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense document type code.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>20</td><td>חשבון / אישור תשלום</td></tr><tr><td>305</td><td>חשבונית מס</td></tr><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>330</td><td>חשבונית זיכוי</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="status"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">status</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpenseStatus)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense status.</p><table><thead><tr><th>Code</th><th>Status</th></tr></thead><tbody><tr><td>10</td><td>הוצאה אושרה לדו״ח</td></tr><tr><td>20</td><td>הוצאה נכללת בדו״ח</td></tr><tr><td>30</td><td>הוצאה שנערכה מחדש</td></tr><tr><td>40</td><td>הוצאה אושרה ע״י מייצג</td></tr><tr><td>100</td><td>הוצאה מחוקה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpensePaymentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense payment method.</p><table><thead><tr><th>Code</th><th>Method</th></tr></thead><tbody><tr><td>-1</td><td>לא שולם</td></tr><tr><td>1</td><td>מזומן</td></tr><tr><td>2</td><td>צ׳ק</td></tr><tr><td>3</td><td>כרטיס אשראי</td></tr><tr><td>4</td><td>העברה בנקאית</td></tr><tr><td>5</td><td>פייפאל</td></tr><tr><td>10</td><td>אפליקציית תשלום</td></tr><tr><td>11</td><td>אחר</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currency"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currency</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Currency)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>3-letter ISO currency code.</p><table><thead><tr><th>Code</th><th>Name</th></tr></thead><tbody><tr><td>ILS</td><td>שקל</td></tr><tr><td>USD</td><td>דולר</td></tr><tr><td>EUR</td><td>אירו</td></tr><tr><td>GBP</td><td>ליש״ט</td></tr><tr><td>JPY</td><td>יין יפני</td></tr><tr><td>CHF</td><td>פרנק שוויצרי</td></tr><tr><td>CNY</td><td>יואן סיני</td></tr><tr><td>AUD</td><td>דולר אוסטרלי</td></tr><tr><td>CAD</td><td>דולר קנדי</td></tr><tr><td>RUB</td><td>רובל</td></tr><tr><td>BRL</td><td>ריאל ברזילאי</td></tr><tr><td>HKD</td><td>דולר הונג קונגי</td></tr><tr><td>SGD</td><td>דולר סינגפורי</td></tr><tr><td>THB</td><td>באט תאילנדי</td></tr><tr><td>MXN</td><td>פזו מקסיקני</td></tr><tr><td>TRY</td><td>לירה טורקית</td></tr><tr><td>NZD</td><td>דולר ניו זילנדי</td></tr><tr><td>SEK</td><td>כתר שבדי</td></tr><tr><td>NOK</td><td>כתר נורבגי</td></tr><tr><td>DKK</td><td>כתר דני</td></tr><tr><td>KRW</td><td>וון דרום קוריאני</td></tr><tr><td>INR</td><td>רופי הודי</td></tr><tr><td>IDR</td><td>רופי אינדונזי</td></tr><tr><td>PLN</td><td>זלוטי</td></tr><tr><td>RON</td><td>לאו רומני</td></tr><tr><td>ZAR</td><td>ראנד דרא״פ</td></tr><tr><td>HRK</td><td>קונה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currencyRate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currencyRate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Exchange rate relative to ILS.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amount</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total amount of the expense, including VAT.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="vat"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">vat</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>VAT portion of the amount.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amountExcludeVat"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amountExcludeVat</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Amount excluding VAT (<code>amount</code> minus <code>vat</code>).</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amountLocal"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amountLocal</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total amount converted to local currency (ILS).</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="deductibleAmount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">deductibleAmount</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Tax-deductible amount, in local currency (ILS).</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="deductibleVat"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">deductibleVat</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Recoverable (input) VAT, in local currency (ILS).</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="date"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">date</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Date of the expense, formatted YYYY-MM-DD.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="reportingDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">reportingDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>VAT reporting date. Always the first day of the month, formatted YYYY-MM-01. For example: <code>2026-05-01</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="number"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">number</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier's document number.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Description of the expense.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="remarks"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">remarks</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Free-text remarks.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="allocationNumber"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">allocationNumber</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Tax Authority Allocation Number, when applicable. For example: <code>166056573</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="supplier"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand supplier"><span class="property-name">supplier</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Supplier)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="accountingClassification"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand accountingClassification"><span class="property-name">accountingClassification</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (AccountingClassification)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Accounting classification (expense category). On the request, send an existing classification's <code>id</code> (from the Get Accounting Classifications endpoint), or the details (<code>irsCode</code>, <code>title</code>, <code>income</code>, <code>vat</code>) to classify inline.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="url"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">url</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Download URL for the attached file. Present only when the expense has an attached file.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="data"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand data"><span class="property-name">data</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Additional expense details.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="creationDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">creationDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Creation date, as a Unix timestamp in seconds.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="lastUpdateDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">lastUpdateDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Last update date, as a Unix timestamp in seconds.</p></div></div></div></td></tr></tbody></table>

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl -X DELETE 'https://api.greeninvoice.co.il/api/v1/expenses/b22f10a6-85f3-4374-b563-e1e039d5528c' \
  -H "Authorization: Bearer $MORNING_ACCESS_TOKEN"
```

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`{  -   "id": "b22f10a6-85f3-4374-b563-e1e039d5528c",      -   "businessId": "c1e4a7b2-8d3f-4a9c-b5e6-3f4a5b6c7d8e",      -   "businessType": 1,      -   "documentType": 320,      -   "status": 10,      -   "paymentType": 3,      -   "currency": "ILS",      -   "currencyRate": 1,      -   "amount": 472,      -   "vat": 72,      -   "amountExcludeVat": 400,      -   "amountLocal": 472,      -   "deductibleAmount": 400,      -   "deductibleVat": 72,      -   "date": "2026-05-06",      -   "reportingDate": "2026-05-01",      -   "number": "100",      -   "description": "אינסטלטור",      -   "remarks": "אינסטלטור-שולם",      -   "allocationNumber": "166056573",      -   "supplier": {          -   "id": "32770ce2-ca0f-469f-87cf-8d92c7826e9b",              -   "name": "ישראל ישראלי",              -   "active": true,              -   "department": "",              -   "taxId": "999317746",              -   "accountingKey": "31653639",              -   "paymentTerms": 0,              -   "bankName": "פועלים",              -   "bankBranch": "123",              -   "bankAccount": "123456",              -   "address": "הרצל 12",              -   "city": "תל אביב",              -   "zip": "6688320",              -   "country": "IL",              -   "phone": "0505555555",              -   "fax": "0504444444",              -   "mobile": "0504444444",              -   "emails": [                  -   "test_test@test.com"                               ],              -   "labels": [                  -   "775c188f-33a1-4d39-a5f2-cf7b82dd5bd5"                               ],              -   "remarks": "",              -   "contactPerson": "ישראל ישראלי",              -   "incomeAmount": 0,              -   "paymentAmount": 0,              -   "creationDate": 1780919300,// 2026-06-08 11:48:20 UTC              -   "lastUpdateDate": 1780919300,// 2026-06-08 11:48:20 UTC              -   "balanceAmount": 0                   },      -   "accountingClassification": {          -   "id": "451b3028-68b7-4d1a-bf63-9bb8be24ca9d",              -   "key": "1310",              -   "code": "1300",              -   "title": "עבודות חוץ וקבלני משנה",              -   "irsCode": 1310,              -   "type": 20,              -   "income": 100,              -   "vat": 100,              -   "mixed": 100,              -   "creationDate": 1771231523,// 2026-02-16 08:45:23 UTC              -   "lastUpdateDate": 1779287537// 2026-05-20 14:32:17 UTC                   },      -   "url": "string",      -   "data": {          -   "labels": [                  -   "string"                               ],              -   "pcnClassification": "T",              -   "pcnTaxId": "990000002"                   },      -   "creationDate": 1780991238,// 2026-06-09 07:47:18 UTC      -   "lastUpdateDate": 1780991238// 2026-06-09 07:47:18 UTC       }`

## Get Allowed Expenses Statuses

get/expenses/statuses

gethttps://api.greeninvoice.co.il/api/v1/expenses/statuses?lang={lang}ProductionSandbox

Retrieve the available expense statuses as a list of `{ id, name }` pairs. Names are localised by the `lang` query parameter.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### query Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="lang"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">lang</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Lang)</span></div><div><span class="sc-Nxspf lmPA-Dn">Enum:</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"he"</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"en"</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">lang=he</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Content language for the localised <code>name</code> field. Defaults to <code>he</code> (Hebrew) if omitted or unsupported.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

List of available expense statuses with localised names

##### Response Schema: application/json

Array

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpenseStatus)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense status.</p><table><thead><tr><th>Code</th><th>Status</th></tr></thead><tbody><tr><td>10</td><td>הוצאה אושרה לדו״ח</td></tr><tr><td>20</td><td>הוצאה נכללת בדו״ח</td></tr><tr><td>30</td><td>הוצאה שנערכה מחדש</td></tr><tr><td>40</td><td>הוצאה אושרה ע״י מייצג</td></tr><tr><td>100</td><td>הוצאה מחוקה</td></tr></tbody></table></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Localised name of the expense status, in the language indicated by the <code>lang</code> query parameter.</p></div></div></div></td></tr></tbody></table>

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl 'https://api.greeninvoice.co.il/api/v1/expenses/statuses' \
  -H "Authorization: Bearer $MORNING_ACCESS_TOKEN"
```

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`[  -   {          -   "id": 10,              -   "name": "הוצאה אושרה לדו״ח"                   },      -   {          -   "id": 20,              -   "name": "הוצאה נכללת בדו״ח"                   },      -   {          -   "id": 30,              -   "name": "הוצאה שנערכה מחדש"                   },      -   {          -   "id": 100,              -   "name": "הוצאה מחוקה"                   },      -   {          -   "id": 40,              -   "name": "הוצאה אושרה ע״י מייצג"                   }       ]`

## Close Expense

post/expenses/{id}/close

posthttps://api.greeninvoice.co.il/api/v1/expenses/{id}/closeProductionSandbox

Close an expense by its ID. No request body is required, and the response returns an empty body.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">b22f10a6-85f3-4374-b563-e1e039d5528c</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense ID</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Expense closed successfully

##### Response Schema: application/json

object

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl -X POST 'https://api.greeninvoice.co.il/api/v1/expenses/b22f10a6-85f3-4374-b563-e1e039d5528c/close' \
  -H "Authorization: Bearer $MORNING_ACCESS_TOKEN"
```

### Response samples

-   200

Content type

application/json

Copy

`{ }`

## Open Expense

post/expenses/{id}/open

posthttps://api.greeninvoice.co.il/api/v1/expenses/{id}/openProductionSandbox

Open an expense by its ID. No request body is required, and the response returns an empty body.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;uuid&gt;</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">b22f10a6-85f3-4374-b563-e1e039d5528c</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense ID</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Expense opened successfully

##### Response Schema: application/json

object

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl -X POST 'https://api.greeninvoice.co.il/api/v1/expenses/b22f10a6-85f3-4374-b563-e1e039d5528c/open' \
  -H "Authorization: Bearer $MORNING_ACCESS_TOKEN"
```

### Response samples

-   200

Content type

application/json

Copy

`{ }`

## Upload Expense File · Step 1: Get Upload URL

get/file-upload/v1/url

gethttps://api.morning.co/file-upload/v1/url?context={context}&data={data}ProductionSandbox

**Step 1 of the expense file-upload flow.** Returns a pre-signed S3 POST (`url` + `fields`) that you use in Step 2 to upload the file. Uploading a file always creates an **expense draft** (which becomes a real expense only after approval).

> **Note:** The pre-signed POST is valid for **60 seconds**. Complete Step 2 within 60 seconds of this request — after that the URL expires and you must request a new one.

-   To create a new draft, send `data={"source":5}`.
-   To attach a file to an existing expense, send `data={"id":"<expenseId>","source":5,"state":"expense"}`.

The upload is processed **asynchronously**; track the outcome via webhooks (`expense-draft/parsed`, `expense-file/updated`, `expense-draft/declined`, `file/infected`).

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### query Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="context"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">context</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">context=expense</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Upload context. Must be <code>expense</code> for the expense file-upload flow.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="data"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">data</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">data={"source":5}</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>JSON string describing the upload. <code>source</code> must be 5. New draft: <code>{"source":5}</code>. Attach to an existing expense: <code>{"id":"&lt;expenseId&gt;","source":5,"state":"expense"}</code>.</p></div></div></div></td></tr></tbody></table>

### Responses

**201**

Pre-signed S3 upload details

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl 'https://api.morning.co/file-upload/v1/url?context=expense&data=%7B%22source%22%3A5%7D' \
  -H "Authorization: Bearer $MORNING_ACCESS_TOKEN"
```

### Response samples

-   201

Content type

application/json

Copy

Expand all Collapse all

`{  -   "url": "[https://s3.eu-west-1.amazonaws.com/string](https://s3.eu-west-1.amazonaws.com/string)",      -   "fields": {          -   "x-amz-meta-account-id": "string",              -   "x-amz-meta-user-id": "string",              -   "x-amz-meta-business-id": "string",              -   "x-amz-meta-file-context": "expense",              -   "x-amz-meta-file-data": "{\"source\":5}",              -   "bucket": "string",              -   "X-Amz-Algorithm": "AWS4-HMAC-SHA256",              -   "X-Amz-Credential": "string",              -   "X-Amz-Date": "string",              -   "X-Amz-Security-Token": "string",              -   "key": "2026/06/09/<businessId>/${filename}",              -   "Policy": "string",              -   "X-Amz-Signature": "string"                   },      -   "maxFileSize": 20971520       }`

## Upload Expense File · Step 2: Send the File

post/

posthttps://s3.eu-west-1.amazonaws.com/file-upload-service-uploaded/ProductionSandbox

**Step 2 of the expense file-upload flow.** Upload the file directly to the `url` returned by [Step 1: Get Upload URL](#operation/getExpenseFileUploadUrl), sending every field from that response's `fields` object as `multipart/form-data` alongside the `file`.

> **Important:** Add the `file` field **last** in the `multipart/form-data` body — after all the other fields. The upload fails if `file` is not the final field.

> **Note:** The pre-signed POST returned in Step 1 is valid for only **60 seconds**. Upload the file within that window, or it expires and you'll need to request a new URL.

Whether this **creates a new expense draft** or **updates an existing expense's file** is determined by the `data` you sent in Step 1. Processing is **asynchronous** — the response is `204 No Content`; track the outcome via webhooks. An expense cannot be updated once it has been reported.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `multipart/form-data` | Yes |

##### Request Body schema: multipart/form-data

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="key"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">key</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="Policy"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">Policy</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="X-Amz-Algorithm"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">X-Amz-Algorithm</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="X-Amz-Credential"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">X-Amz-Credential</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="X-Amz-Date"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">X-Amz-Date</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="X-Amz-Security-Token"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">X-Amz-Security-Token</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="X-Amz-Signature"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">X-Amz-Signature</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="bucket"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">bucket</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="file"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">file</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;binary&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The file to upload.</p></div></div></div></td></tr></tbody></table>

### Responses

**204**

File accepted for processing

### Request samples

-   Payload
-   Helper Script

Content type

multipart/form-data

Copy

```
{
  "key": "2026/06/09/c1e4a7b2-8d3f-4a9c-b5e6-3f4a5b6c7d8e/${filename}",
  "Policy": "string",
  "X-Amz-Algorithm": "AWS4-HMAC-SHA256",
  "X-Amz-Credential": "string",
  "X-Amz-Date": "20260609T130133Z",
  "X-Amz-Security-Token": "string",
  "X-Amz-Signature": "string",
  "bucket": "string",
  "file": "<the file to upload>"
}
```

## Search Expense Drafts

post/expenses/drafts/search

posthttps://api.greeninvoice.co.il/api/v1/expenses/drafts/searchProductionSandbox

Search the current business's expense drafts with optional filters. Results are paginated.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="fromDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">fromDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Start of the creation date range to filter by, formatted YYYY-MM-DD.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="toDate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">toDate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>End of the creation date range to filter by, formatted YYYY-MM-DD.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by expense draft description.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="supplierId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">supplierId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by supplier ID.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="supplierName"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">supplierName</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by supplier name. For example: <code>שפע</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="page"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">page</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Page number to retrieve (1-based). Defaults to 1.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pageSize"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pageSize</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Number of results per page.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Paginated list of expense drafts matching the search

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="total"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">total</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total number of expense drafts matching the search.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="page"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">page</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The page number returned.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pageSize"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pageSize</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The number of results per page.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pages"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pages</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total number of pages available.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="from"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">from</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>1-based index of the first item on this page.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="to"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">to</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>1-based index of the last item on this page.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="items"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand items"><span class="property-name">items</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpenseDraft)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The expense drafts matching the search.</p></div></div></div></td></tr></tbody></table>

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

`{  -   "fromDate": "2026-03-01",      -   "toDate": "2026-06-30",      -   "description": "string",      -   "supplierId": "string",      -   "supplierName": "שפע",      -   "page": 1,      -   "pageSize": 20       }`

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`{  -   "total": 1,      -   "page": 1,      -   "pageSize": 20,      -   "pages": 1,      -   "from": 1,      -   "to": 1,      -   "items": [          -   {                  -   "id": "315fd195-8703-486d-a883-88adfd434429",                      -   "businessId": "c1e4a7b2-8d3f-4a9c-b5e6-3f4a5b6c7d8e",                      -   "status": 10,                      -   "expense": {                          -   "documentType": 320,                              -   "number": "1003024467",                              -   "date": "2026-03-15T00:00:00",                              -   "reportingDate": "2026-03-01T00:00:00",                              -   "paymentType": 3,                              -   "currency": "ILS",                              -   "currencyRate": 1,                              -   "amount": 49.9,                              -   "vat": 7.61,                              -   "description": "string",                              -   "texts": [                                  -   "string"                                                       ],                              -   "supplier": {                                  -   "id": "32770ce2-ca0f-469f-87cf-8d92c7826e9b",                                      -   "name": "ישראל ישראלי",                                      -   "active": true,                                      -   "department": "",                                      -   "taxId": "999317746",                                      -   "accountingKey": "31653639",                                      -   "paymentTerms": 0,                                      -   "bankName": "פועלים",                                      -   "bankBranch": "123",                                      -   "bankAccount": "123456",                                      -   "address": "הרצל 12",                                      -   "city": "תל אביב",                                      -   "zip": "6688320",                                      -   "country": "IL",                                      -   "phone": "0505555555",                                      -   "fax": "0504444444",                                      -   "mobile": "0504444444",                                      -   "emails": [                                          -   "test_test@test.com"                                                                   ],                                      -   "labels": [                                          -   "775c188f-33a1-4d39-a5f2-cf7b82dd5bd5"                                                                   ],                                      -   "remarks": "",                                      -   "contactPerson": "ישראל ישראלי",                                      -   "incomeAmount": 0,                                      -   "paymentAmount": 0,                                      -   "creationDate": 1780919300,// 2026-06-08 11:48:20 UTC                                      -   "lastUpdateDate": 1780919300,// 2026-06-08 11:48:20 UTC                                      -   "balanceAmount": 0                                                       },                              -   "accountingClassification": {                                  -   "id": "451b3028-68b7-4d1a-bf63-9bb8be24ca9d",                                      -   "key": "1310",                                      -   "code": "1300",                                      -   "title": "עבודות חוץ וקבלני משנה",                                      -   "irsCode": 1310,                                      -   "type": 20,                                      -   "income": 100,                                      -   "vat": 100,                                      -   "mixed": 100,                                      -   "creationDate": 1771231523,// 2026-02-16 08:45:23 UTC                                      -   "lastUpdateDate": 1779287537// 2026-05-20 14:32:17 UTC                                                       },                              -   "active": true,                              -   "addRecipient": true                                           },                      -   "reportingPeriod": "03-04/2026",                      -   "url": "string",                      -   "creationDate": 1781013227,// 2026-06-09 13:53:47 UTC                      -   "lastUpdateDate": 1781015771// 2026-06-09 14:36:11 UTC                               }                   ]       }`

## Payments

Collect payments from your customers — generate a hosted payment form to share with a customer, and manage and charge saved credit-card tokens.

## Get Payment Form

post/payments/form

posthttps://api.greeninvoice.co.il/api/v1/payments/formProductionSandbox

Create a payment request and return a payment form URL you can present to the customer — as an iframe or a redirect — to collect a payment. Once the customer pays, the configured document is created automatically.

The `group` field is required only when using the Digital Payments (Grow) plugin. If no `pluginId` is provided, the business's default payment plugin is used.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Description of the document created for this payment. For example: <code>Payment for order #1024</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="type"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">type</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (PaidDocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document type that can be created through a payment.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr><tr><td>600</td><td>קבלת פיקדון</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amount</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The amount the customer needs to pay. Must be greater than 0. For example: 20.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currency"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currency</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (PaidCurrency)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>3-letter ISO currency code supported for payments.</p><table><thead><tr><th>Code</th><th>Name</th></tr></thead><tbody><tr><td>ILS</td><td>שקל</td></tr><tr><td>USD</td><td>דולר</td></tr><tr><td>EUR</td><td>אירו</td></tr><tr><td>GBP</td><td>ליש״ט</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="vatType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">vatType</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentVatType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document-level VAT type.</p><table><thead><tr><th>Value</th><th>Meaning</th></tr></thead><tbody><tr><td>0</td><td>Default (based on business type)</td></tr><tr><td>1</td><td>Exempt (VAT-free)</td></tr><tr><td>2</td><td>Mixed (contains both exempt and taxable rows)</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="lang"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">lang</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Lang)</span></div><div><span class="sc-Nxspf lmPA-Dn">Enum:</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"he"</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"en"</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Content language</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="client"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand client"><span class="property-name">client</span></button><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Client information</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="maxPayments"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">maxPayments</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Number of credit-card installments, between 1 and 36. Defaults to 1.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pluginId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pluginId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The clearing plugin ID to use. If omitted, the business's default payment plugin is used. For example: <code>7944827a-c664-11e4-8231-080027271115</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="group"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">group</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (PaymentFormGroup)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Payment method offered on the payment form.</p><table><thead><tr><th>Code</th><th>Group</th></tr></thead><tbody><tr><td>100</td><td>Credit Card</td></tr><tr><td>110</td><td>PayPal</td></tr><tr><td>120</td><td>Bit</td></tr><tr><td>150</td><td>Google Pay</td></tr><tr><td>160</td><td>Apple Pay</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="income"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand income"><span class="property-name">income</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (MinimalIncomeRowRequest)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Income (line-item) rows. If no rows are provided, a single row is created from the request's <code>description</code> and <code>amount</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="remarks"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">remarks</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Remarks shown on the created document. For example: <code>Some remarks</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="successUrl"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">successUrl</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>HTTPS URL the customer is redirected to after a successful payment. For example: <code>https://example.com/success</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="failureUrl"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">failureUrl</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>HTTPS URL the customer is redirected to after a failed payment. For example: <code>https://example.com/failure</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="notifyUrl"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">notifyUrl</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>HTTPS URL notified (POST) once the payment succeeds and the document is created. For example: <code>https://example.com/notify</code>.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="custom"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">custom</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Custom data echoed back to your success / failure / notify URLs, such as an internal order ID. For example: <code>order-1024</code>.</p></div></div></div></td></tr></tbody></table>

### Responses

**201**

Payment form URL created successfully

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

Expand all Collapse all

`{  -   "description": "Payment for order #1024",      -   "type": 320,      -   "amount": 20,      -   "currency": "ILS",      -   "vatType": 0,      -   "lang": "he",      -   "maxPayments": 1,      -   "pluginId": "7944827a-c664-11e4-8231-080027271115",      -   "group": 100,      -   "client": {          -   "id": "7944827a-c664-11e4-8231-080027271114",              -   "name": "John Doe",              -   "emails": [                  -   "email1@example.com",                      -   "email2@example.com"                               ],              -   "taxId": "0123456789",              -   "address": "1 Luria St",              -   "city": "Tel Aviv",              -   "zip": "1234567",              -   "country": "IL",              -   "phone": "+972-54-1234567",              -   "fax": "+972-54-1234567",              -   "mobile": "+972-54-1234567",              -   "add": false                   },      -   "income": [          -   {                  -   "catalogNum": "MXDFSDD",                      -   "description": "Item description",                      -   "quantity": 1,                      -   "price": 20,                      -   "currency": "ILS",                      -   "vatType": 1                               }                   ],      -   "remarks": "Some remarks",      -   "successUrl": "[https://example.com/success](https://example.com/success)",      -   "failureUrl": "[https://example.com/failure](https://example.com/failure)",      -   "notifyUrl": "[https://example.com/notify](https://example.com/notify)",      -   "custom": "order-1024"       }`

### Response samples

-   201

Content type

application/json

Copy

`{  -   "success": true,      -   "errorCode": 0,      -   "errorDescription": "string",      -   "url": "[https://payments.example.com/checkout/1a2b3c4d](https://payments.example.com/checkout/1a2b3c4d)"       }`

## Search Credit Card Tokens

post/payments/tokens/search

posthttps://api.greeninvoice.co.il/api/v1/payments/tokens/searchProductionSandbox

Search the saved credit-card tokens of the current business using any combination of the filters in the request body. All filters are optional; omitting the body returns the most recent tokens. Results are paginated.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### Request Body schema: application/json

optional

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="page"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">page</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><span class="sc-Nxspf lmPA-Dn">Default: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">1</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Page number to retrieve. Defaults to 1.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pageSize"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pageSize</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><span class="sc-Nxspf lmPA-Dn">Default: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">25</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Number of results per page. Defaults to 25.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentNumber"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentNumber</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by the card's last 4 digits. For example: <code>0000</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="cardHolder"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">cardHolder</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by card holder name. For example: <code>John Doe</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="externalKey"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">externalKey</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by the client ID the token is associated with. For example: <code>b0077e19-977b-4389-a2e1-f84fa0527d23</code>.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="cardType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">cardType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integers</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (CreditCardType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Filter by credit card brand(s).</p><table><thead><tr><th>Code</th><th>Brand</th></tr></thead><tbody><tr><td>0</td><td>Unknown</td></tr><tr><td>1</td><td>Isracard</td></tr><tr><td>2</td><td>Visa</td></tr><tr><td>3</td><td>Mastercard</td></tr><tr><td>4</td><td>American Express</td></tr><tr><td>5</td><td>Diners</td></tr></tbody></table></div></div></div></td></tr></tbody></table>

### Responses

**200**

Paginated list of credit-card tokens matching the search

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="total"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">total</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total number of tokens matching the search</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="page"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">page</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The requested page number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pageSize"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pageSize</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The requested page size</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="from"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">from</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Index of the first token in the current page</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="to"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">to</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Index of the last token in the current page</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pages"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pages</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total number of pages available</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="items"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand items"><span class="property-name">items</span></button><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (CreditCardToken)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The credit-card tokens matching the search</p></div></div></div></td></tr></tbody></table>

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

Expand all Collapse all

`{  -   "page": 1,      -   "pageSize": 25,      -   "paymentNumber": "0000",      -   "cardHolder": "John Doe",      -   "externalKey": "b0077e19-977b-4389-a2e1-f84fa0527d23",      -   "cardType": [          -   2                   ]       }`

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`{  -   "total": 1,      -   "page": 1,      -   "pageSize": 25,      -   "from": 1,      -   "to": 1,      -   "pages": 1,      -   "items": [          -   {                  -   "id": "46e78fc4-9d8c-4429-9748-454947be39cb",                      -   "externalKey": "b0077e19-977b-4389-a2e1-f84fa0527d23",                      -   "clientName": "John Doe",                      -   "status": 1,                      -   "cardType": 2,                      -   "number": "0000",                      -   "expires": "0129",                      -   "holderName": "John Doe",                      -   "pluginType": 12100,                      -   "currencies": [                          -   "ILS"                                           ],                      -   "creationDate": 1765186595,// 2025-12-08 09:36:35 UTC                      -   "lastUpdateDate": 1765186595// 2025-12-08 09:36:35 UTC                               }                   ]       }`

## Charge Credit Card Token

post/payments/tokens/{id}/charge

posthttps://api.greeninvoice.co.il/api/v1/payments/tokens/{id}/chargeProductionSandbox

Charge a saved credit-card token. A document of the requested type is created and returned once the charge succeeds.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Bearer <accessToken>` | Yes |

##### Authorizations:

_bearerAuth_

##### path Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">8b338c95-095e-46d4-b2c6-331747508759</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The credit-card token ID to charge.</p></div></div></div></td></tr></tbody></table>

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="type"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">type</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (PaidDocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document type that can be created through a payment.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr><tr><td>600</td><td>קבלת פיקדון</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="amount"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">amount</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The amount to charge. Must be greater than 0. For example: 20.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currency"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currency</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (PaidCurrency)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>3-letter ISO currency code supported for payments.</p><table><thead><tr><th>Code</th><th>Name</th></tr></thead><tbody><tr><td>ILS</td><td>שקל</td></tr><tr><td>USD</td><td>דולר</td></tr><tr><td>EUR</td><td>אירו</td></tr><tr><td>GBP</td><td>ליש״ט</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="vatType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">vatType</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentVatType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document-level VAT type.</p><table><thead><tr><th>Value</th><th>Meaning</th></tr></thead><tbody><tr><td>0</td><td>Default (based on business type)</td></tr><tr><td>1</td><td>Exempt (VAT-free)</td></tr><tr><td>2</td><td>Mixed (contains both exempt and taxable rows)</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="lang"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">lang</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Lang)</span></div><div><span class="sc-Nxspf lmPA-Dn">Enum:</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"he"</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"en"</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Content language</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Description of the document created for this charge. For example: <code>Transaction description</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="maxPayments"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">maxPayments</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Number of credit-card installments, between 1 and 36. Defaults to 1.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="income"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand income"><span class="property-name">income</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (MinimalIncomeRowRequest)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Income (line-item) rows. If no rows are provided, a single row is created from the request's <code>description</code> and <code>amount</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="remarks"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">remarks</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Remarks shown on the created document. For example: <code>Some remarks</code>.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="notifyUrl"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">notifyUrl</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>HTTPS URL notified (POST) once the payment succeeds and the document is created. For example: <code>https://example.com/notify</code>.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

The document created by the charge

##### Response Schema: application/json

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document unique ID</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="number"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">number</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document serial number</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="type"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">type</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document type code.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>10</td><td>הצעת מחיר</td></tr><tr><td>20</td><td>חשבון / אישור תשלום</td></tr><tr><td>100</td><td>הזמנה</td></tr><tr><td>200</td><td>תעודת משלוח</td></tr><tr><td>210</td><td>תעודת החזרה</td></tr><tr><td>300</td><td>חשבון עסקה</td></tr><tr><td>305</td><td>חשבונית מס</td></tr><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>330</td><td>חשבונית זיכוי</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr><tr><td>410</td><td>ביטול תרומה</td></tr><tr><td>500</td><td>הזמנת רכש</td></tr><tr><td>600</td><td>קבלת פיקדון</td></tr><tr><td>610</td><td>משיכת פיקדון</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="signed"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">signed</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether the document was digitally signed</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="lang"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">lang</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Lang)</span></div><div><span class="sc-Nxspf lmPA-Dn">Enum:</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"he"</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"en"</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Content language</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="client"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand client"><span class="property-name">client</span></button><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Client linked to the document</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="url"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand url"><span class="property-name">url</span></button><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document download URLs</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="taxAuthorityConfirmationInitiated"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">taxAuthorityConfirmationInitiated</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether tax authority confirmation was initiated for the document</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="taxAuthorityConfirmationLastError"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">taxAuthorityConfirmationLastError</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Error code from the most recent tax authority confirmation attempt. <code>0</code> indicates no error; a non-zero value (for example <code>400</code> or <code>406</code>) indicates a failure.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="vatRate"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">vatRate</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>VAT rate applied to the document</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="transactionId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">transactionId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The payment transaction ID.</p></div></div></div></td></tr></tbody></table>

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

Expand all Collapse all

`{  -   "description": "Transaction description",      -   "type": 320,      -   "amount": 20,      -   "currency": "ILS",      -   "vatType": 0,      -   "lang": "he",      -   "maxPayments": 1,      -   "income": [          -   {                  -   "catalogNum": "MXDFSDD",                      -   "description": "Item description",                      -   "quantity": 1,                      -   "price": 20,                      -   "currency": "ILS",                      -   "vatType": 1                               }                   ],      -   "remarks": "Some remarks",      -   "notifyUrl": "[https://example.com/notify](https://example.com/notify)"       }`

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`{  -   "id": "57ae2ff9-0c24-43e8-b39c-a5bdcc05573d",      -   "number": 40034,      -   "type": 305,      -   "signed": true,      -   "lang": "he",      -   "client": {          -   "id": "7944827a-c664-11e4-8231-080027271114"                   },      -   "taxAuthorityConfirmationInitiated": false,      -   "url": {          -   "origin": "string",              -   "he": "string",              -   "en": "string"                   },      -   "taxAuthorityConfirmationLastError": 0,      -   "vatRate": 0.18,      -   "transactionId": "feac32ae-cfda-422c-8502-3adc2cd2e261"       }`

## Partners

> -   Performing actions in user accounts is restricted to **existing users in morning with a `Best` subscription plan or higher**.
> -   Currently, partners are unable to create new user accounts.

To use the Partners endpoints you must be a Green Invoice partner. Contact Green Invoice to obtain your partner authorization code.

A Green Invoice partner can connect third-party applications to Green Invoice and control connected users through their application.

**How it works — 3 steps:**

1.  **Request authorization** from an existing morning by Green Invoice user. Call `POST /partners/users/connection` — the user receives an email with a connection approval link valid for 3 days. Once approved, Green Invoice sends a `POST` request to the `url` you specified. Its body contains the connected user's `id`, `email`, and a `key` object holding the business's newly created API key (its `id` and `secret`) — store the key securely, as you exchange it for an access token in step 2.
2.  **Obtain a JWT** for the user by calling [`POST /idp/v1/oauth/token`](#tag/Authentication/operation/obtainAccessToken) with the user's API key ID as `client_id` and the secret as `client_secret`.
3.  **Control the user** by using the returned `accessToken` as a `Bearer` token in the `Authorization` header of any subsequent API request.

**Security note:** The approval callback includes an `X-Data-Signature` header — the SHA-256 HMAC of the request body, signed with your partner authorization code as the key. Compare it against your own HMAC computation to verify the callback's authenticity. This step is optional but recommended.

![Request User Approval Flowchart](https://cdn.greeninvoice.co.il/files/ugc/4/c/1/4c1131ed83cd40a9a174078429d4b2e7.png)

> **Note:** An inactive partner account will result in a `403 Forbidden` response.

## Get Connected Users

get/partners/users

gethttps://api.greeninvoice.co.il/api/v1/partners/usersProductionSandbox

Returns all connected and approved users for your partner account.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Basic <credentials>` | Yes |

##### Authorizations:

_basicAuth_

### Responses

**200**

Connected users retrieved successfully

##### Response Schema: application/json

Array

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The connected user's masked identifier.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="email"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">email</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The connected user's email address.</p></div></div></div></td></tr></tbody></table>

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl 'https://api.greeninvoice.co.il/api/v1/partners/users' \
  -H "Authorization: Bearer $MORNING_ACCESS_TOKEN"
```

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`[  -   {          -   "id": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4",              -   "email": "user@example.com"                   }       ]`

## Request User Approval

post/partners/users/connection

posthttps://api.greeninvoice.co.il/api/v1/partners/users/connection?email={email}ProductionSandbox

Sends a connection request to an existing morning by Green Invoice user.

The user receives an email with a link to approve the connection. The link expires after 3 days — if it is not approved in time, a new request must be initiated.

Once the user approves, Green Invoice sends a `POST` request to the `url` you specified. The body contains the connected user's `id`, `email`, and a `key` object holding the business's newly created API key — including its `id` and `secret`. An `X-Data-Signature` header is also included — the SHA-256 HMAC of the body using your partner authorization code as the key — which you can use to verify the callback's authenticity.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Basic <credentials>` | Yes |

##### Authorizations:

_basicAuth_

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="email"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">email</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The email address of the morning user to invite. For example: <code>user@example.com</code>.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="url"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">url</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The callback URL where Green Invoice will send the connection approval notification. For example: <code>https://example.com/callback</code>.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Connection request sent successfully

### Request samples

-   Payload
-   cURL
-   Node.js
-   Python

Content type

application/json

Copy

`{  -   "email": "user@example.com",      -   "url": "[https://example.com/callback](https://example.com/callback)"       }`

## Disconnect Partner User

delete/partners/users/connection

deletehttps://api.greeninvoice.co.il/api/v1/partners/users/connection?email={email}ProductionSandbox

Removes a connected user from your partner account.

All partner-related API keys for the user's businesses are revoked and you will no longer be able to access their resources. If the user is billed through your partner account, billing stops immediately for future documents.

The user receives a notification email upon disconnection. A disconnected user may reconnect at any time.

> **Note:** All businesses of the specified user that are associated with your partner will be disconnected.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |
| `Authorization` | `Basic <credentials>` | Yes |

##### Authorizations:

_basicAuth_

##### query Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="email"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">email</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">email=user@example.com</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The email address of the connected user to disconnect. For example: <code>user@example.com</code>.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

User disconnected successfully

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl -X DELETE 'https://api.greeninvoice.co.il/api/v1/partners/users/connection?email=user%40example.com' \
  -H "Authorization: Bearer $MORNING_ACCESS_TOKEN"
```

## Webhooks

Webhooks let your application receive real-time notifications when events happen in morning — for example, when a document is created.

Unlike the rest of the API, webhooks are **configured in the morning interface**, not through an API call:

1.  In morning, open **[Developer Tools → Webhooks](https://app.greeninvoice.co.il/settings/developers/webhooks)**.
2.  Click **Add Webhook**, give it a name, and enter the **URL** on your server that should receive the notifications.
3.  Choose one or more **events** to subscribe to. Optionally, set a **secret** used to sign every delivery so you can verify it came from morning (see **Verifying deliveries** below). Then save.

Once saved, every subscribed event triggers an HTTP `POST` to your URL with a JSON body describing the event.

**Delivery headers**

Every delivery includes the following headers:

| Header | Description |
| --- | --- |
| `x-webhook-topic` | The event type, e.g. `document/created`. |
| `x-webhook-id` | Identifier of the webhook configuration that produced the delivery. |
| `x-webhook-delivery-id` | Unique identifier of this specific delivery. |
| `x-webhook-timestamp` | Time the event was emitted, in ISO 8601 format. |
| `x-correlation-id` | Correlation identifier, useful for support and debugging. |
| `user-agent` | Always `morning webhooks` followed by the version, e.g. `morning webhooks 2.1`. |
| `x-webhook-signature` | Present only when the webhook is configured with a secret — an HMAC-SHA256 signature of the delivered body. See **Verifying deliveries** below. |

**Verifying deliveries**

When a webhook has a **secret**, every delivery carries an `x-webhook-signature` header — the HMAC-SHA256 of the raw request body, keyed with your secret, hex-encoded.

To verify, compute the same HMAC over the **raw** received bytes and compare with a constant-time comparison. Capture the raw body before any JSON parsing — re-serializing parsed JSON changes the bytes and breaks the signature.

Example (Node.js / Express):

```javascript
const crypto = require('crypto');
const express = require('express');
const app = express();

// Capture the raw body exactly as received — do NOT let a JSON parser re-serialize it.
app.use(express.raw({ type: 'application/json' }));

app.post('/webhook', (req, res) => {
    const rawBody = req.body; // Buffer of the exact bytes received
    const signature = req.get('x-webhook-signature');
    const expected = crypto.createHmac('sha256', secret).update(rawBody).digest('hex');

    const isValid = signature &&
        crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(signature));
    if (!isValid) return res.status(401).send('invalid signature');

    const event = JSON.parse(rawBody.toString('utf8'));
    // ... handle the event
    res.sendStatus(200);
});
```

**Delivery failures**

Acknowledge each delivery by responding with one of `200`, `201`, `202`, or `204`. Any other response — including `3xx` redirects and other status codes — is treated as a failed delivery, as are timeouts and connection errors.

Failed deliveries are counted; after 15 failures the webhook becomes inactive and stops receiving events.

**Available events**

| Event | Triggered when |
| --- | --- |
| `document/created` | A document is created. |
| `client/created` | A client is created. |
| `supplier/created` | A supplier is created. |
| `payment/received` | A payment is received. |
| `sale-pages/page-contacted` | A visitor submits their contact details on a sale page. |
| `sale-pages/order-paid` | An order is paid on a sale page. |
| `expense-draft/parsed` | An uploaded expense draft finishes parsing. |
| `expense-draft/declined` | An uploaded expense draft is declined. |
| `expense/file-updated` | An expense's file is updated. |
| `file/infected` | An uploaded file is found to be infected and quarantined. |

## Document Created Webhook

Sent to your configured webhook URL whenever a document is created in a subscribed business.

The `x-webhook-topic` header on this delivery is `document/created`.

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unique identifier of the created document.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="type"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">type</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (DocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document type code.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>10</td><td>הצעת מחיר</td></tr><tr><td>20</td><td>חשבון / אישור תשלום</td></tr><tr><td>100</td><td>הזמנה</td></tr><tr><td>200</td><td>תעודת משלוח</td></tr><tr><td>210</td><td>תעודת החזרה</td></tr><tr><td>300</td><td>חשבון עסקה</td></tr><tr><td>305</td><td>חשבונית מס</td></tr><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>330</td><td>חשבונית זיכוי</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr><tr><td>410</td><td>ביטול תרומה</td></tr><tr><td>500</td><td>הזמנת רכש</td></tr><tr><td>600</td><td>קבלת פיקדון</td></tr><tr><td>610</td><td>משיכת פיקדון</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="number"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">number</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document serial number.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="businessId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">businessId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unique identifier of the business that issued the document.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="businessType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">businessType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (BusinessType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Business type.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>1</td><td>עוסק מורשה</td></tr><tr><td>2</td><td>חברה בע״מ</td></tr><tr><td>3</td><td>עוסק פטור</td></tr><tr><td>4</td><td>עמותה</td></tr><tr><td>5</td><td>חברה לתועלת הציבור</td></tr><tr><td>6</td><td>שותפות</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currency"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currency</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Currency)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>3-letter ISO currency code.</p><table><thead><tr><th>Code</th><th>Name</th></tr></thead><tbody><tr><td>ILS</td><td>שקל</td></tr><tr><td>USD</td><td>דולר</td></tr><tr><td>EUR</td><td>אירו</td></tr><tr><td>GBP</td><td>ליש״ט</td></tr><tr><td>JPY</td><td>יין יפני</td></tr><tr><td>CHF</td><td>פרנק שוויצרי</td></tr><tr><td>CNY</td><td>יואן סיני</td></tr><tr><td>AUD</td><td>דולר אוסטרלי</td></tr><tr><td>CAD</td><td>דולר קנדי</td></tr><tr><td>RUB</td><td>רובל</td></tr><tr><td>BRL</td><td>ריאל ברזילאי</td></tr><tr><td>HKD</td><td>דולר הונג קונגי</td></tr><tr><td>SGD</td><td>דולר סינגפורי</td></tr><tr><td>THB</td><td>באט תאילנדי</td></tr><tr><td>MXN</td><td>פזו מקסיקני</td></tr><tr><td>TRY</td><td>לירה טורקית</td></tr><tr><td>NZD</td><td>דולר ניו זילנדי</td></tr><tr><td>SEK</td><td>כתר שבדי</td></tr><tr><td>NOK</td><td>כתר נורבגי</td></tr><tr><td>DKK</td><td>כתר דני</td></tr><tr><td>KRW</td><td>וון דרום קוריאני</td></tr><tr><td>INR</td><td>רופי הודי</td></tr><tr><td>IDR</td><td>רופי אינדונזי</td></tr><tr><td>PLN</td><td>זלוטי</td></tr><tr><td>RON</td><td>לאו רומני</td></tr><tr><td>ZAR</td><td>ראנד דרא״פ</td></tr><tr><td>HRK</td><td>קונה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="country"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">country</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>2-letter ISO 3166-1 alpha-2 country code of the issuing business. See the <a href="#operation/getSupportedCountries">Get Supported Countries</a> endpoint for the full list.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="date"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">date</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;date&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document date, in <code>YYYY-MM-DD</code> format.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="createdAt"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">createdAt</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unix timestamp in milliseconds of when the document was created.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="subtotal"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">subtotal</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document total before VAT.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="taxableTotal"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">taxableTotal</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total amount subject to VAT.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="vatTaxableTotal"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">vatTaxableTotal</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total amount subject to VAT (currently identical to <code>taxableTotal</code>).</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="revenueTaxableTotal"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">revenueTaxableTotal</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total revenue subject to income tax.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="exemptTotal"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">exemptTotal</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total of the VAT-exempt amounts.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="rounding"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">rounding</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether the document amounts are rounded.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="custom"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand custom"><span class="property-name">custom</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Custom data attached to the document. Omitted when no custom data was set.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="bill"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand bill"><span class="property-name">bill</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Present when the document is linked to a payment request; omitted otherwise.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="discount"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand discount"><span class="property-name">discount</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document-level discount. Omitted when no discount was applied.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="tax"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand tax"><span class="property-name">tax</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Tax breakdown lines. Contains a VAT line when VAT applies.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="total"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">total</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document total, including VAT.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Document title.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="remarks"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">remarks</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Free-text remarks shown on the document.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="reverseCharge"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">reverseCharge</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether reverse-charge VAT applies to the document.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="recipient"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand recipient"><span class="property-name">recipient</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The party the document was issued to.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="items"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand items"><span class="property-name">items</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The document line items.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="transactionId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">transactionId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Identifier of the source transaction that triggered the document. Omitted when the document was not generated from a transaction.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="transactions"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand transactions"><span class="property-name">transactions</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Payment transactions recorded on the document. Empty when the document has no payments.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="files"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand files"><span class="property-name">files</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The document's generated files.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="allocationNumber"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">allocationNumber</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Israeli Tax Authority allocation (confirmation) number, when one was assigned to the document. Omitted otherwise.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="foreignCurrencyRate"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand foreignCurrencyRate"><span class="property-name">foreignCurrencyRate</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Exchange rate from the document currency to the local currency (ILS), keyed by the 3-letter local currency code. Present only when the document currency is not ILS.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="generatedBy"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand generatedBy"><span class="property-name">generatedBy</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The user who generated the document.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Return any `2xx` status code to acknowledge that your endpoint received the event.

### Request samples

-   Payload

Content type

application/json

Copy

Expand all Collapse all

`{  -   "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",      -   "type": 320,      -   "number": 60873,      -   "businessId": "9b7c1e42-8d3a-4f16-b0c5-1e2d3a4b5c6d",      -   "businessType": 2,      -   "currency": "ILS",      -   "country": "IL",      -   "date": "2026-07-01",      -   "createdAt": 1782893748000,// 2026-07-01 08:15:48 UTC      -   "subtotal": 300,      -   "taxableTotal": 300,      -   "vatTaxableTotal": 300,      -   "revenueTaxableTotal": 300,      -   "exemptTotal": 0,      -   "rounding": false,      -   "tax": [          -   {                  -   "name": "VAT",                      -   "rate": 0.18,                      -   "total": 54                               }                   ],      -   "total": 354,      -   "description": "",      -   "remarks": "Tax invoice / receipt for transaction invoice 40000468",      -   "reverseCharge": false,      -   "recipient": {          -   "id": "5c1f2e3d-4b5a-4c6d-9e8f-0a1b2c3d4e5f",              -   "name": "David Levi",              -   "taxId": "514987326",              -   "department": "",              -   "address": "1 Main St",              -   "city": "Nahariya",              -   "zip": "18555",              -   "country": "IL",              -   "phone": "03-1234567",              -   "mobile": "",              -   "emails": [                  -   "david@example.com"                               ]                   },      -   "items": [          -   {                  -   "description": "UI design hour",                      -   "sku": "UI-001",                      -   "quantity": 1,                      -   "price": 300,                      -   "currency": "ILS",                      -   "taxIncludedInPrice": false,                      -   "tax": [                          -   {                                  -   "name": "VAT",                                      -   "rate": 0.18                                                       }                                           ]                               }                   ],      -   "transactionId": "7e8d9c0b-1a2f-4e3d-8c5b-6a7f8e9d0c1b",      -   "transactions": [          -   {                  -   "id": "2b3c4d5e-6f70-4819-a2b3-c4d5e6f70819",                      -   "price": 354,                      -   "currency": "ILS",                      -   "date": "2026-07-01",                      -   "paymentMethod": {                          -   "type": "credit-card",                              -   "cardNumber": "0008"                                           }                               }                   ],      -   "files": {          -   "signed": true,              -   "downloadLinks": {                  -   "he": "[https://www.greeninvoice.co.il/api/v1/documents/download?d=...](https://www.greeninvoice.co.il/api/v1/documents/download?d=...)",                      -   "en": "[https://www.greeninvoice.co.il/api/v1/documents/download?d=...](https://www.greeninvoice.co.il/api/v1/documents/download?d=...)",                      -   "origin": "[https://www.greeninvoice.co.il/api/v1/documents/download?d=...](https://www.greeninvoice.co.il/api/v1/documents/download?d=...)"                               }                   },      -   "generatedBy": {          -   "id": "8a2f1c3e-4d5b-4e6f-9a0b-1c2d3e4f5a6b",              -   "name": "Noa Cohen"                   }       }`

## Client Created Webhook

Sent to your configured webhook URL whenever a client is created in a subscribed business.

The `x-webhook-topic` header on this delivery is `client/created`.

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unique identifier of the client.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Client name.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="taxId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">taxId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Client tax ID.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="department"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">department</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Client department.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="address"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">address</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Street address.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="city"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">city</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>City.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="zip"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">zip</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Postal code.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="country"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">country</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>2-letter ISO 3166-1 alpha-2 country code. See the <a href="#operation/getSupportedCountries">Get Supported Countries</a> endpoint for the full list.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="phone"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">phone</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Phone number.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="mobile"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">mobile</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Mobile number.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="emails"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">emails</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Client email addresses.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="contact"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">contact</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Contact person name.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="createdAt"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">createdAt</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unix timestamp in milliseconds of when the client was created.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="updatedAt"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">updatedAt</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unix timestamp in milliseconds of when the client was last updated.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Return any `2xx` status code to acknowledge that your endpoint received the event.

### Request samples

-   Payload

Content type

application/json

Copy

Expand all Collapse all

`{  -   "id": "8a1b2c3d-4e5f-4061-9273-8495a6b7c8d9",      -   "name": "Dana Cohen",      -   "taxId": "512345678",      -   "department": "Finance",      -   "address": "1 Main St",      -   "city": "Tel Aviv",      -   "zip": "6120101",      -   "country": "IL",      -   "phone": "03-0000000",      -   "mobile": "050-0000000",      -   "emails": [          -   "client@example.com"                   ],      -   "contact": "Dana",      -   "createdAt": 1782896238000,// 2026-07-01 08:57:18 UTC      -   "updatedAt": 1782896238000// 2026-07-01 08:57:18 UTC       }`

## Supplier Created Webhook

Sent to your configured webhook URL whenever a supplier is created in a subscribed business.

The `x-webhook-topic` header on this delivery is `supplier/created`.

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unique identifier of the supplier.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Supplier name.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="taxId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">taxId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Supplier tax ID.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="department"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">department</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Supplier department.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="address"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">address</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Street address.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="city"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">city</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>City.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="zip"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">zip</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Postal code.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="country"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">country</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>2-letter ISO 3166-1 alpha-2 country code. See the <a href="#operation/getSupportedCountries">Get Supported Countries</a> endpoint for the full list.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="phone"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">phone</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Phone number.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="mobile"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">mobile</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Mobile number.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="emails"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">emails</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Supplier email addresses.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="contact"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">contact</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Contact person name.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="createdAt"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">createdAt</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unix timestamp in milliseconds of when the supplier was created.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="updatedAt"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">updatedAt</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unix timestamp in milliseconds of when the supplier was last updated.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Return any `2xx` status code to acknowledge that your endpoint received the event.

### Request samples

-   Payload

Content type

application/json

Copy

Expand all Collapse all

`{  -   "id": "4d5e6f70-8192-4a3b-b5c6-d7e8f9012345",      -   "name": "Global Supplies Ltd",      -   "taxId": "515263748",      -   "department": "Finance",      -   "address": "10 Trade Ave",      -   "city": "Kyiv",      -   "zip": "01001",      -   "country": "UA",      -   "phone": "03-0000000",      -   "mobile": "050-0000000",      -   "emails": [          -   "supplier@example.com"                   ],      -   "contact": "Alex",      -   "createdAt": 1782896493000,// 2026-07-01 09:01:33 UTC      -   "updatedAt": 1782896493000// 2026-07-01 09:01:33 UTC       }`

## Payment Received Webhook

Sent to your configured webhook URL whenever a payment is received in a subscribed business.

The `x-webhook-topic` header on this delivery is `payment/received`.

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unique identifier of the payment request.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="channel"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">channel</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The channel the payment was made through, e.g. <code>sale-page</code>.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="productId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">productId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>External product identifier associated with the payment, when applicable.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Description of the payment request.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="total"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">total</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Total amount paid.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="custom"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand custom"><span class="property-name">custom</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Custom data attached to the payment request. Omitted when none was set.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="payer"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand payer"><span class="property-name">payer</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The party that made the payment.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="transactions"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand transactions"><span class="property-name">transactions</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The payment transactions that make up this payment.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Return any `2xx` status code to acknowledge that your endpoint received the event.

### Request samples

-   Payload

Content type

application/json

Copy

Expand all Collapse all

`{  -   "id": "6f708192-a3b4-4c5d-9e6f-708192a3b4c5",      -   "channel": "sale-page",      -   "description": "Purchase from sale page",      -   "total": 210,      -   "payer": {          -   "name": "Dana Cohen",              -   "email": "payer@example.com"                   },      -   "transactions": [          -   {                  -   "id": "0c1b2a3d-4e5f-4607-8918-2a3b4c5d6e7f",                      -   "createdAt": 1782896958000,// 2026-07-01 09:09:18 UTC                      -   "currency": "ILS",                      -   "gateway": "cardcom",                      -   "gatewayTransactionId": "900112233",                      -   "installments": 1,                      -   "total": 210,                      -   "authorizationCode": "12345",                      -   "payer": {                          -   "name": "Card Owner"                                           },                      -   "paymentMethod": {                          -   "type": "credit-card",                              -   "cardNumber": "0008"                                           }                               }                   ]       }`

## Sale Page Contacted Webhook

Sent to your configured webhook URL whenever a visitor submits their details on a sale page in a subscribed business. This covers both sale-page blocks that collect visitor details — the **contact** block and the **newsletter-signup** block — which share the same payload. Which fields are populated depends on the block and its configuration; `newsletter` indicates whether the visitor opted into the mailing list.

The `x-webhook-topic` header on this delivery is `sale-pages/page-contacted`.

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="firstName"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">firstName</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>First name entered in the contact form.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="lastName"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">lastName</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Last name entered in the contact form.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="email"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">email</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Email address entered in the contact form.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="phone"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">phone</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Phone number entered in the contact form.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="newsletter"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">newsletter</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether the visitor opted in to the business's mailing list, consenting to receive marketing content by email and/or SMS.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="message"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">message</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Free-text message entered by the visitor. Present only when the block includes a message field.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pageName"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pageName</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Name of the sale page the contact request was submitted from.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="streams"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">streams</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integers</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Integration (plugin) type codes the contact request was forwarded to. Empty when none are configured.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Return any `2xx` status code to acknowledge that your endpoint received the event.

### Request samples

-   Payload

Content type

application/json

Copy

Expand all Collapse all

`{  -   "firstName": "Dana",      -   "lastName": "Cohen",      -   "email": "dana@example.com",      -   "phone": "050-0000000",      -   "newsletter": true,      -   "message": "What are your opening hours?",      -   "pageName": "My Store",      -   "streams": [ ]       }`

## Sale Page Order Paid Webhook

Sent to your configured webhook URL whenever an order is paid on a sale page in a subscribed business.

The `x-webhook-topic` header on this delivery is `sale-pages/order-paid`.

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="businessId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">businessId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unique identifier of the business that owns the sale page.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="pageId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">pageId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unique identifier of the sale page.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="documentId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">documentId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unique identifier of the document created for the order, when one was created.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="orderNumber"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">orderNumber</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Sequential order number.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Order description.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="billing"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand billing"><span class="property-name">billing</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The customer's billing details.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="shipping"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand shipping"><span class="property-name">shipping</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The shipping details, when the order includes shipping.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="tax"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand tax"><span class="property-name">tax</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>VAT breakdown for the order.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="transactions"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand transactions"><span class="property-name">transactions</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The payment recorded for the order.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="items"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand items"><span class="property-name">items</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The ordered line items.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="discount"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand discount"><span class="property-name">discount</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Order-level coupon discount. Present only when a coupon was applied.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="createdAt"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">createdAt</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unix timestamp in milliseconds of when the order was created.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paidAt"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paidAt</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unix timestamp in milliseconds of when the order was paid.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Return any `2xx` status code to acknowledge that your endpoint received the event.

### Request samples

-   Payload

Content type

application/json

Copy

Expand all Collapse all

`{  -   "businessId": "a1c2e3f4-5b6d-4e7f-8a9b-0c1d2e3f4a5b",      -   "pageId": "b2d3f4a5-6c7e-4f8a-9b0c-1d2e3f4a5b6c",      -   "documentId": "c3e4a5b6-7d8f-4a9b-8c0d-2e3f4a5b6c7d",      -   "orderNumber": 7708,      -   "description": "Purchase from sale page",      -   "billing": {          -   "name": "Dana Cohen",              -   "email": "dana@example.com",              -   "taxId": "514987326",              -   "nameOnInvoice": "Dana Cohen",              -   "notes": "Please gift-wrap"                   },      -   "shipping": {          -   "name": "Dana Cohen",              -   "phone": "050-0000000",              -   "address": {                  -   "formatted": "12 Herzl St, Tel Aviv, 6120101, Israel",                      -   "city": "Tel Aviv",                      -   "country": "IL",                      -   "street": "Herzl",                      -   "streetNumber": 12,                      -   "entrance": "A",                      -   "postalCode": "6120101",                      -   "apartmentNumber": 5                               },              -   "method": "Israel Post",              -   "price": 10,              -   "currency": "ILS",              -   "notes": "Leave at the door"                   },      -   "tax": [          -   {                  -   "name": "VAT",                      -   "rate": 0.18                               }                   ],      -   "transactions": {          -   "price": 210,              -   "currency": "ILS",              -   "paymentMethod": "credit-card"                   },      -   "items": [          -   {                  -   "name": "Sample product 1",                      -   "description": "Product item",                      -   "quantity": 2,                      -   "price": 100,                      -   "currency": "ILS",                      -   "discount": {                          -   "total": null,                              -   "type": "none"                                           }                               }                   ],      -   "createdAt": 1782896952762,// 2026-07-01 09:09:12 UTC      -   "paidAt": 1782896953000// 2026-07-01 09:09:13 UTC       }`

## Expense Draft Parsed Webhook

Sent to your configured webhook URL whenever an uploaded expense draft finishes parsing in a subscribed business.

The `x-webhook-topic` header on this delivery is `expense-draft/parsed`.

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unique identifier of the expense draft.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="createdAt"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">createdAt</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unix timestamp in milliseconds of when the draft was created.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="updatedAt"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">updatedAt</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unix timestamp in milliseconds of when the draft was last updated.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="status"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">status</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpenseDraftStatus)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense draft status.</p><table><thead><tr><th>Code</th><th>Status</th></tr></thead><tbody><tr><td>10</td><td>חדש</td></tr><tr><td>50</td><td>נכשל</td></tr><tr><td>200</td><td>נדחה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="recognized"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">recognized</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether the draft was recognized and populated with default values from parsing.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="thumbnail"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">thumbnail</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>URL of the draft's thumbnail image.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="url"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">url</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>URL to download the draft's source file.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="subtotal"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">subtotal</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense total before VAT.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="total"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">total</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense total, including VAT.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="number"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">number</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense document number.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="source"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">source</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense source code.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense description.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="remarks"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">remarks</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Free-text remarks on the expense.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="classification"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand classification"><span class="property-name">classification</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The accounting classification assigned to the expense.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="prediction"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand prediction"><span class="property-name">prediction</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The parsing (OCR) prediction result.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="documentType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">documentType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpenseDocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense document type code.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>20</td><td>חשבון / אישור תשלום</td></tr><tr><td>305</td><td>חשבונית מס</td></tr><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>330</td><td>חשבונית זיכוי</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="uploadTrackingId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">uploadTrackingId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Identifier correlating the draft with the original upload.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="tax"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand tax"><span class="property-name">tax</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>VAT breakdown for the expense.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currency"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currency</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Currency)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>3-letter ISO currency code.</p><table><thead><tr><th>Code</th><th>Name</th></tr></thead><tbody><tr><td>ILS</td><td>שקל</td></tr><tr><td>USD</td><td>דולר</td></tr><tr><td>EUR</td><td>אירו</td></tr><tr><td>GBP</td><td>ליש״ט</td></tr><tr><td>JPY</td><td>יין יפני</td></tr><tr><td>CHF</td><td>פרנק שוויצרי</td></tr><tr><td>CNY</td><td>יואן סיני</td></tr><tr><td>AUD</td><td>דולר אוסטרלי</td></tr><tr><td>CAD</td><td>דולר קנדי</td></tr><tr><td>RUB</td><td>רובל</td></tr><tr><td>BRL</td><td>ריאל ברזילאי</td></tr><tr><td>HKD</td><td>דולר הונג קונגי</td></tr><tr><td>SGD</td><td>דולר סינגפורי</td></tr><tr><td>THB</td><td>באט תאילנדי</td></tr><tr><td>MXN</td><td>פזו מקסיקני</td></tr><tr><td>TRY</td><td>לירה טורקית</td></tr><tr><td>NZD</td><td>דולר ניו זילנדי</td></tr><tr><td>SEK</td><td>כתר שבדי</td></tr><tr><td>NOK</td><td>כתר נורבגי</td></tr><tr><td>DKK</td><td>כתר דני</td></tr><tr><td>KRW</td><td>וון דרום קוריאני</td></tr><tr><td>INR</td><td>רופי הודי</td></tr><tr><td>IDR</td><td>רופי אינדונזי</td></tr><tr><td>PLN</td><td>זלוטי</td></tr><tr><td>RON</td><td>לאו רומני</td></tr><tr><td>ZAR</td><td>ראנד דרא״פ</td></tr><tr><td>HRK</td><td>קונה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="country"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">country</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>2-letter ISO 3166-1 alpha-2 country code. See the <a href="#operation/getSupportedCountries">Get Supported Countries</a> endpoint for the full list.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="foreignCurrencyRate"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand foreignCurrencyRate"><span class="property-name">foreignCurrencyRate</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Exchange rate from the expense currency to the local currency (ILS), keyed by the 3-letter local currency code. Present only when the expense currency is not ILS.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="date"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">date</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;date&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense date, in <code>YYYY-MM-DD</code> format.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="recipient"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand recipient"><span class="property-name">recipient</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier the expense was issued by.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="reportingPeriod"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">reportingPeriod</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The reporting period the expense is associated with, in <code>YYYY-MM</code> format.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Return any `2xx` status code to acknowledge that your endpoint received the event.

### Request samples

-   Payload

Content type

application/json

Copy

Expand all Collapse all

`{  -   "id": "d1e2f3a4-5b6c-4d7e-8f90-1a2b3c4d5e6f",      -   "createdAt": 1782900153000,// 2026-07-01 10:02:33 UTC      -   "updatedAt": 1782900153000,// 2026-07-01 10:02:33 UTC      -   "status": 10,      -   "recognized": true,      -   "thumbnail": "[https://www.greeninvoice.co.il/api/v1/expenses/thumbnail?d=...](https://www.greeninvoice.co.il/api/v1/expenses/thumbnail?d=...)",      -   "url": "[https://www.greeninvoice.co.il/api/v1/expenses/download?d=...&ft=1](https://www.greeninvoice.co.il/api/v1/expenses/download?d=...&ft=1)",      -   "subtotal": 1,      -   "total": 1.18,      -   "number": "50002",      -   "source": 1,      -   "description": "",      -   "classification": {          -   "type": 20,              -   "irsCode": 1390,              -   "title": "Other costs",              -   "code": "1300",              -   "key": "1390",              -   "income": 100,              -   "vat": 100                   },      -   "prediction": {          -   "origin": "ocr",              -   "fields": [                  -   {                          -   "field": "amount",                              -   "value": 1.18,                              -   "confidence": "high",                              -   "coordinates": [ ]                                           },                      -   {                          -   "field": "net",                              -   "value": 1,                              -   "confidence": "high",                              -   "coordinates": [                                  -   {                                          -   "top": 38,                                              -   "left": 17                                                                   },                                      -   {                                          -   "top": 38,                                              -   "left": 20                                                                   },                                      -   {                                          -   "top": 39,                                              -   "left": 20                                                                   },                                      -   {                                          -   "top": 39,                                              -   "left": 17                                                                   }                                                       ]                                           },                      -   {                          -   "field": "supplier",                              -   "confidence": "low",                              -   "coordinates": [ ]                                           }                               ]                   },      -   "documentType": 305,      -   "uploadTrackingId": "e2f3a4b5-6c7d-4e8f-9a0b-1c2d3e4f5a6b",      -   "tax": [          -   {                  -   "name": "VAT",                      -   "rate": 0.18,                      -   "total": 0.18                               }                   ],      -   "currency": "USD",      -   "country": "IL",      -   "foreignCurrencyRate": {          -   "ILS": 3.65                   },      -   "date": "2026-06-26",      -   "recipient": {          -   "id": "f0e1d2c3-b4a5-4968-8778-6a5b4c3d2e1f",              -   "name": "Acme Supplies Ltd.",              -   "country": "IL",              -   "emails": [ ]                   },      -   "reportingPeriod": "2026-06"       }`

## Expense Draft Declined Webhook

Sent to your configured webhook URL whenever an accountant declines an uploaded expense draft — i.e. does not approve it for intake — in a subscribed business.

The `x-webhook-topic` header on this delivery is `expense-draft/declined`.

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="hash"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">hash</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Hash of the uploaded file.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="format"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">format</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>File format / extension of the uploaded file.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="mimeType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">mimeType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>MIME type of the uploaded file.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="size"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">size</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Size of the uploaded file, in bytes.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="errorCode"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">errorCode</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Numeric code associated with the decline.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="reason"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">reason</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Short machine-readable token for the decline.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="referenceId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">referenceId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Human-readable text describing why the accountant declined the draft.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="uploadTrackingId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">uploadTrackingId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Identifier correlating the draft with the original upload.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Return any `2xx` status code to acknowledge that your endpoint received the event.

### Request samples

-   Payload

Content type

application/json

Copy

`{  -   "hash": "9f8e7d6c5b4a3210fedcba9876543210",      -   "format": "pdf",      -   "mimeType": "application/pdf",      -   "size": 190519,      -   "errorCode": 3308,      -   "reason": "",      -   "referenceId": "Invalid expense document type",      -   "uploadTrackingId": "a2b3c4d5-e6f7-4809-9a1b-2c3d4e5f6a7b"       }`

## Expense File Updated Webhook

Sent to your configured webhook URL whenever the file of an **already-approved expense** is updated in a subscribed business. This fires only for an approved expense — updating the file of an expense **draft** does not trigger it.

The `x-webhook-topic` header on this delivery is `expense/file-updated`.

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unique identifier of the expense.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="number"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">number</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense document number.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="businessId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">businessId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unique identifier of the business that owns the expense.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="businessType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">businessType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (BusinessType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Business type.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>1</td><td>עוסק מורשה</td></tr><tr><td>2</td><td>חברה בע״מ</td></tr><tr><td>3</td><td>עוסק פטור</td></tr><tr><td>4</td><td>עמותה</td></tr><tr><td>5</td><td>חברה לתועלת הציבור</td></tr><tr><td>6</td><td>שותפות</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="createdAt"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">createdAt</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unix timestamp in milliseconds of when the expense was created.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="updatedAt"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">updatedAt</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unix timestamp in milliseconds of when the expense was last updated.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="active"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">active</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">boolean</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Whether the expense is active.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="status"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">status</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpenseStatus)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense status.</p><table><thead><tr><th>Code</th><th>Status</th></tr></thead><tbody><tr><td>10</td><td>הוצאה אושרה לדו״ח</td></tr><tr><td>20</td><td>הוצאה נכללת בדו״ח</td></tr><tr><td>30</td><td>הוצאה שנערכה מחדש</td></tr><tr><td>40</td><td>הוצאה אושרה ע״י מייצג</td></tr><tr><td>100</td><td>הוצאה מחוקה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="documentType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">documentType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpenseDocumentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense document type code.</p><table><thead><tr><th>Code</th><th>Type</th></tr></thead><tbody><tr><td>20</td><td>חשבון / אישור תשלום</td></tr><tr><td>305</td><td>חשבונית מס</td></tr><tr><td>320</td><td>חשבונית מס / קבלה</td></tr><tr><td>330</td><td>חשבונית זיכוי</td></tr><tr><td>400</td><td>קבלה</td></tr><tr><td>405</td><td>קבלה על תרומה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="thumbnail"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">thumbnail</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>URL of the expense's thumbnail image.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="url"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">url</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>URL to download the expense's source file.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="subtotal"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">subtotal</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense total before VAT.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="total"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">total</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">number</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense total, including VAT.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="classification"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand classification"><span class="property-name">classification</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The accounting classification assigned to the expense.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="currency"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">currency</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (Currency)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>3-letter ISO currency code.</p><table><thead><tr><th>Code</th><th>Name</th></tr></thead><tbody><tr><td>ILS</td><td>שקל</td></tr><tr><td>USD</td><td>דולר</td></tr><tr><td>EUR</td><td>אירו</td></tr><tr><td>GBP</td><td>ליש״ט</td></tr><tr><td>JPY</td><td>יין יפני</td></tr><tr><td>CHF</td><td>פרנק שוויצרי</td></tr><tr><td>CNY</td><td>יואן סיני</td></tr><tr><td>AUD</td><td>דולר אוסטרלי</td></tr><tr><td>CAD</td><td>דולר קנדי</td></tr><tr><td>RUB</td><td>רובל</td></tr><tr><td>BRL</td><td>ריאל ברזילאי</td></tr><tr><td>HKD</td><td>דולר הונג קונגי</td></tr><tr><td>SGD</td><td>דולר סינגפורי</td></tr><tr><td>THB</td><td>באט תאילנדי</td></tr><tr><td>MXN</td><td>פזו מקסיקני</td></tr><tr><td>TRY</td><td>לירה טורקית</td></tr><tr><td>NZD</td><td>דולר ניו זילנדי</td></tr><tr><td>SEK</td><td>כתר שבדי</td></tr><tr><td>NOK</td><td>כתר נורבגי</td></tr><tr><td>DKK</td><td>כתר דני</td></tr><tr><td>KRW</td><td>וון דרום קוריאני</td></tr><tr><td>INR</td><td>רופי הודי</td></tr><tr><td>IDR</td><td>רופי אינדונזי</td></tr><tr><td>PLN</td><td>זלוטי</td></tr><tr><td>RON</td><td>לאו רומני</td></tr><tr><td>ZAR</td><td>ראנד דרא״פ</td></tr><tr><td>HRK</td><td>קונה</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="country"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">country</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>2-letter ISO 3166-1 alpha-2 country code. See the <a href="#operation/getSupportedCountries">Get Supported Countries</a> endpoint for the full list.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="tax"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand tax"><span class="property-name">tax</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>VAT breakdown for the expense.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="date"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">date</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;date&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense date, in <code>YYYY-MM-DD</code> format.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="recipient"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand recipient"><span class="property-name">recipient</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The supplier the expense was issued by.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="paymentType"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">paymentType</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (ExpensePaymentType)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense payment method.</p><table><thead><tr><th>Code</th><th>Method</th></tr></thead><tbody><tr><td>-1</td><td>לא שולם</td></tr><tr><td>1</td><td>מזומן</td></tr><tr><td>2</td><td>צ׳ק</td></tr><tr><td>3</td><td>כרטיס אשראי</td></tr><tr><td>4</td><td>העברה בנקאית</td></tr><tr><td>5</td><td>פייפאל</td></tr><tr><td>10</td><td>אפליקציית תשלום</td></tr><tr><td>11</td><td>אחר</td></tr></tbody></table></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="allocationNumber"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">allocationNumber</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Israeli Tax Authority allocation (confirmation) number assigned to the expense.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="transactionId"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">transactionId</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Identifier of the transaction associated with the expense, when applicable.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="description"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">description</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Expense description.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="foreignCurrencyRate"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand foreignCurrencyRate"><span class="property-name">foreignCurrencyRate</span></button></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Exchange rate from the expense currency to the local currency (ILS), keyed by the 3-letter local currency code. Present only when the expense currency is not ILS.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Return any `2xx` status code to acknowledge that your endpoint received the event.

### Request samples

-   Payload

Content type

application/json

Copy

Expand all Collapse all

`{  -   "id": "aa11bb22-cc33-4d44-8e55-6f778899aabb",      -   "number": "5001",      -   "businessId": "9b7c1e42-8d3a-4f16-b0c5-1e2d3a4b5c6d",      -   "businessType": 2,      -   "createdAt": 1778148284000,// 2026-05-07 10:04:44 UTC      -   "updatedAt": 1780417007000,// 2026-06-02 16:16:47 UTC      -   "active": true,      -   "status": 20,      -   "documentType": 20,      -   "thumbnail": "[https://www.greeninvoice.co.il/api/v1/expenses/thumbnail?d=...](https://www.greeninvoice.co.il/api/v1/expenses/thumbnail?d=...)",      -   "url": "[https://www.greeninvoice.co.il/api/v1/expenses/download?d=...&ft=2](https://www.greeninvoice.co.il/api/v1/expenses/download?d=...&ft=2)",      -   "subtotal": 100,      -   "total": 100,      -   "classification": {          -   "id": "c1d2e3f4-a5b6-4c7d-8e9f-0a1b2c3d4e5f",              -   "irsCode": 1306,              -   "title": "Domestic purchases",              -   "code": "200",              -   "key": "200",              -   "income": 100,              -   "vat": 66.67,              -   "mixed": 100                   },      -   "currency": "ILS",      -   "country": "IL",      -   "tax": [          -   {                  -   "name": "VAT",                      -   "rate": 0.18,                      -   "total": 0                               }                   ],      -   "date": "2026-05-06",      -   "recipient": {          -   "id": "d4e5f6a7-b8c9-4d0e-8f1a-2b3c4d5e6f70",              -   "name": "ACME Ltd",              -   "taxId": "",              -   "department": "",              -   "address": "",              -   "city": "",              -   "zip": "",              -   "country": "IL",              -   "mobile": "",              -   "emails": [ ],              -   "contact": "",              -   "createdAt": 1770296985000,// 2026-02-05 13:09:45 UTC              -   "updatedAt": 1778148616000// 2026-05-07 10:10:16 UTC                   },      -   "allocationNumber": "",      -   "description": ""       }`

## File Infected Webhook

Sent to your configured webhook URL whenever an uploaded file is found to be infected and quarantined in a subscribed business.

The `x-webhook-topic` header on this delivery is `file/infected`.

##### Request Body schema: application/json

required

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Storage key of the quarantined file (URL-encoded); the path segments include the date and business identifier.</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="key"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">key</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Storage key of the quarantined file (identical to <code>name</code>).</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="data"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">data</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>A JSON-encoded string of file metadata, e.g. <code>{"source":1,"uploadTrackingId":"..."}</code>. Parse it to read fields such as <code>source</code> and <code>uploadTrackingId</code>.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Return any `2xx` status code to acknowledge that your endpoint received the event.

### Request samples

-   Payload

Content type

application/json

Copy

`{  -   "name": "2026/07/01/9b7c1e42-8d3a-4f16-b0c5-1e2d3a4b5c6d/receipt.pdf",      -   "key": "2026/07/01/9b7c1e42-8d3a-4f16-b0c5-1e2d3a4b5c6d/receipt.pdf",      -   "data": "{\"source\":1,\"uploadTrackingId\":\"a1b2c3d4-e5f6-4708-9192-a3b4c5d6e7f8\"}"       }`

## Reference

Reference data endpoints — lookup values such as supported countries, currencies, and business categories.

> **Note:** All endpoints under **Reference** are served from the shared cache host (`cache.greeninvoice.co.il`), which is the same across all environments — there is no separate sandbox host. Authentication is not required.

## Get Supported Business Categories

get/businesses/v1/occupations

gethttps://cache.greeninvoice.co.il/businesses/v1/occupations?locale={locale}

Get all supported business categories and their sub-categories, ordered alphabetically by the localized name.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |

##### query Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="locale"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">locale</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><span class="sc-Nxspf lmPA-Dn">Enum:</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"en_US"</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"he_IL"</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">locale=he_IL</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Content language for the localized <code>name</code> and <code>keywords</code> fields</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

List of supported business categories

##### Response Schema: application/json

Array

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The business category code (also used as the sub-category code for nested entries)</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="updatedAt"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">updatedAt</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unix timestamp in milliseconds of when the category was last updated</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The localized category name</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="keywords"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">keywords</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">strings</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Localized search keywords associated with the category. Omitted when the category has none.</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="children"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">children</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK">Array of </span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">objects</span><span class="sc-Nxspf sc-gmPhUn lmPA-Dn loPURS"> (BusinessCategory)</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Sub-categories of this category. Present only on top-level categories that have sub-categories; sub-categories themselves have no children.</p></div></div></div></td></tr></tbody></table>

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl 'https://cache.greeninvoice.co.il/businesses/v1/occupations?locale=he_IL'
```

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`[  -   {          -   "id": 22,              -   "updatedAt": 1718054936930,// 2024-06-10 21:28:56 UTC              -   "name": "אבטחה וחקירות",              -   "keywords": [                  -   "חוקר"                               ],              -   "children": [                  -   {                          -   "id": 2201,                              -   "updatedAt": 1718054936931,// 2024-06-10 21:28:56 UTC                              -   "name": "שירותי אבטחה",                              -   "keywords": [                                  -   "מאבטח"                                                       ]                                           },                      -   {                          -   "id": 2202,                              -   "updatedAt": 1718054936931,// 2024-06-10 21:28:56 UTC                              -   "name": "שירותי חקירה",                              -   "keywords": [                                  -   "חוקר"                                                       ]                                           }                               ]                   }       ]`

## Get Supported Countries

get/geo-location/v1/countries

gethttps://cache.greeninvoice.co.il/geo-location/v1/countries?locale={locale}

Get all supported countries, ordered alphabetically by the localized country name.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |

##### query Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="locale"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">locale</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><span class="sc-Nxspf lmPA-Dn">Enum:</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"en_US"</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"he_IL"</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">locale=he_IL</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Content language for the localized <code>name</code> field</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

List of supported countries

##### Response Schema: application/json

Array

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="alpha2code"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">alpha2code</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>2-letter ISO 3166-1 alpha-2 country code</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="alpha3code"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">alpha3code</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>3-letter ISO 3166-1 alpha-3 country code</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The country full name in the requested language</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="callingCode"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">callingCode</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>International dialing code</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="updatedAt"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">updatedAt</span></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unix timestamp in milliseconds of the last update to this record</p></div></div></div></td></tr></tbody></table>

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl 'https://cache.greeninvoice.co.il/geo-location/v1/countries?locale=he_IL'
```

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`[  -   {          -   "alpha2code": "IL",              -   "alpha3code": "ISR",              -   "callingCode": 972,              -   "name": "ישראל",              -   "updatedAt": 1718049888858// 2024-06-10 20:04:48 UTC                   }       ]`

## Get Supported Cities

get/geo-location/v1/cities

gethttps://cache.greeninvoice.co.il/geo-location/v1/cities?locale={locale}&country={country}

Get all supported cities for a given country, ordered alphabetically by the localized city name.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |

##### query Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="locale"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">locale</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><span class="sc-Nxspf lmPA-Dn">Enum:</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"en_US"</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"he_IL"</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">locale=he_IL</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Content language for the localized <code>name</code> field</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="country"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">country</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><span class="sc-Nxspf lmPA-Dn">Value:</span> <span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">"IL"</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">country=IL</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>2-letter ISO 3166-1 alpha-2 country code. Currently only <code>IL</code> (Israel) is supported.</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

List of supported cities

##### Response Schema: application/json

Array

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="country"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">country</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The 2-letter code of the country</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="id"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">id</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The ID of the city object</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="name"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">name</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The name of the city in the specified locale</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="updatedAt"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">updatedAt</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unix timestamp in milliseconds of the last update to this record</p></div></div></div></td></tr></tbody></table>

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl 'https://cache.greeninvoice.co.il/geo-location/v1/cities?locale=he_IL&country=IL'
```

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`[  -   {          -   "country": "IL",              -   "id": 284,              -   "updatedAt": 1718052025380,// 2024-06-10 20:40:25 UTC              -   "name": "שדה ורבורג"                   }       ]`

## Get Supported Currencies

get/currency-exchange/v1/latest

gethttps://cache.greeninvoice.co.il/currency-exchange/v1/latest?base={base}

Get the latest and previous-day exchange rates for supported currencies, relative to a specified base currency.

**Request headers**

| Header | Value | Required |
| --- | --- | --- |
| `Content-Type` | `application/json` | Yes |

##### query Parameters

<table class="sc-dAbbOL kPNSPV"><tbody><tr class="last"><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="base"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">base</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><span class="sc-Nxspf lmPA-Dn">Example: </span><span class="sc-Nxspf sc-ddjGPC lmPA-Dn hiqTjp">base=ILS</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>3-letter currency code of the base currency</p></div></div></div></td></tr></tbody></table>

### Responses

**200**

Latest exchange rates for the supported currencies

##### Response Schema: application/json

Array

<table class="sc-dAbbOL kPNSPV"><tbody><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="base"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">base</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The base currency code</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="code"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">code</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The currency code</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="symbol"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">symbol</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">string</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>The currency symbol</p></div></div></div></td></tr><tr class=""><td class="sc-dLMFU sc-eldPxv eixvFh iOOLXn" kind="field" title="updatedAt"><span class="sc-gFqAkR fbSPvC"></span><span class="property-name">updatedAt</span><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">integer</span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM"> &lt;int64&gt;</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Unix timestamp in milliseconds of the last update to this record</p></div></div></div></td></tr><tr class="last"><td class="sc-dLMFU sc-eldPxv sc-hCPjZK eixvFh iOOLXn fuoyue" kind="field" title="rates"><span class="sc-gFqAkR fbSPvC"></span><button aria-label="expand rates"><span class="property-name">rates</span></button><div class="sc-Nxspf sc-hRJfrW lmPA-Dn fgKwaR">required</div></td><td class="sc-fPXMVe duomj"><div><div><span class="sc-Nxspf sc-cfxfcM lmPA-Dn hHOUkK"></span><span class="sc-Nxspf sc-gFAWRd lmPA-Dn bXvgrM">object</span></div><div><div class="sc-eeDRCY sc-eBMEME gvJSKt gmYFHH"><p>Exchange rate information for this currency</p></div></div></div></td></tr></tbody></table>

### Request samples

-   cURL
-   Node.js
-   Python

Copy

```
curl 'https://cache.greeninvoice.co.il/currency-exchange/v1/latest?base=ILS'
```

### Response samples

-   200

Content type

application/json

Copy

Expand all Collapse all

`[  -   {          -   "base": "ILS",              -   "code": "USD",              -   "symbol": "$",              -   "updatedAt": 1720265835875,// 2024-07-06 11:37:15 UTC              -   "rates": {                  -   "spot": {                          -   "current": 3.693908,                              -   "previous": 3.679988,                              -   "change": 0.01392,                              -   "changePercent": 0.378262                                           },                      -   "closing": {                          -   "current": 3.693908,                              -   "previous": 3.679988,                              -   "change": 0.01392,                              -   "changePercent": 0.378262                                           }                               }                   }       ]`

## Errors

Green Invoice system is in Hebrew language and therefore the errors you will receive are in Hebrew.

We have added a list for you to view of the error code numbers and their descriptions (the descriptions are in Hebrew).

| Error Code | Description |
| --- | --- |
| 401 | גישה נדחתה, נא להתחבר מחדש. |
| 1002 | שדה שם ריק. |
| 1003 | לא נמצא עסק פעיל בחשבון. |
| 1004 | Empty request body or invalid JSON. |
| 1005 | שגיאה במהלך שמירה. |
| 1006 | נא לחדש את המינוי. |
| 1007 | חסרה הרשאה מתאימה. |
| 403 | גישה אסורה. |
| 404 | פריט לא נמצא. |
| 405 | Method Not Allowed. |
| 1008 | פריט לא עודכן, כיוון שלא בוצעו שינויים. |
| 1009 | יש לבחור כתובות מייל. |
| 1010 | קיימת כבר בקשה עם נתונים זהים. |
| 1011 | שפה לא נתמכת. |
| 1012 | פעולה זו נתמכת במינוי גבוה יותר. |
| 1013 | קובץ ריק או לא תקין. |
| 1014 | סוג קובץ לא נתמך. |
| 1015 | יש להסדיר את החוב בחשבון על מנת לבצע את הפעולה. |
| 1016 | שגיאה בעדכון בסיס נתונים. |
| 1017 | שגיאה כללית. |
| 1018 | שגיאה בשליחת מייל. יתכן וכתובת המייל חסומה או לא תקינה. |
| 1019 | כתובת המייל של הנמען חסומה לשליחה. |
| 1020 | שגיאת הצפנה. |
| 1100 | שדה {id} לא תקין |
| 1101 | לא נשלחו שדות לעדכון. |
| 1102 | כתובת מייל לא תקינה. |
| 1103 | כתובת אתר לא תקינה. |
| 1104 | קוד מדינה לא תקין. |
| 1105 | ערך תנאי תשלום לא תקין. |
| 1106 | ערך קוד מטבע לא תקין. |
| 1107 | שער המרה לא תקין, ערך צריך להיות גדול מאפס. |
| 1108 | שיעור מע"מ לא תקין. צריך להיות בין 0-1. |
| 1109 | קיימת שורה עם מע"מ במסמך ללא מע"מ. |
| 1110 | מחיר לא תקין. |
| 2000 | החשבון עדיין לא פעיל. |
| 2001 | משתמש חסום. |
| 2002 | מייל או סיסמה לא נכונים. |
| 2003 | משתמש לא קיים. |
| 2004 | נא למלא שם פרטי. |
| 2005 | נא למלא שם משפחה. |
| 2006 | סיסמה לא תקינה. צריכה להיות 8-16 ספרות או תווים. |
| 2007 | מייל תפוס. |
| 2008 | סיסמה נוכחית לא נכונה. |
| 2009 | מספר ת.ז. לא תקין. |
| 2010 | החשבון כבר הופעל. |
| 2012 | ערך id לא תקין. |
| 2013 | ערך type לא תקין. |
| 2014 | נתוני מפתח לא נכונים. |
| 1111 | מספר עוסק / ח.פ אינו תקין. |
| 1112 | לא ניתן להוסיף מסמכים. בחודש זה הופקה כמות המסמכים המירבית לחשבון. |
| 1113 | שדה תקבול לא נשלח. |
| 1114 | תאריך התחלה לא תקין. |
| 1115 | תאריך סיום לא תקין. |
| 1116 | סכום מע״מ לא תקין. |
| 1117 | תאריך לא תקין. |
| 1118 | לא ניתן לרכוש שירותים נוספים ללא מסלול פעיל בתשלום. |
| 1119 | גודל עמוד צריך להיות לכל היותר 100. |
| 1120 | כתובת הדומיין של המייל לא תקינה. |
| 2100 | סוג עוסק לא תקין. |
| 2101 | שם העסק לא יכול להיות ריק. |
| 2102 | לא ניתן להוסיף עוד עסקים במסגרת המינוי. |
| 2103 | נא למלא כתובת עסק. |
| 2104 | נא למלא עיר. |
| 2105 | קובץ לא תקין או גדול מ 5M. |
| 2106 | סוג קובץ לא נתמך. |
| 2107 | מספר תבנית עיצוב לא תקין. |
| 2125 | מספר סקין בתבנית עיצוב לא תקין. |
| 2126 | אחוז מקדמות אינו תקין. ערך תקין הוא מספר בין 0-35. |
| 2127 | ערך תחום עיסוק לא תקין. |
| 2128 | ערך מקצוע לא תקין. |
| 2129 | ערך סדר עיצוב שדות תקבולים במסמך לא תקין. |
| 2108 | לא נמצא עסק. |
| 2109 | מספר סניף בנק יכול להכיל עד 5 תווים. |
| 2110 | עסק עם שם זהה כבר רשום בחשבון. |
| 2111 | מספר עוסק / ח.פ כבר קיים בחשבון. |
| 2112 | מספר עוסק / ח.פ כבר קיים במערכת תחת חשבון אחר. |
| 2113 | מספר עוסק / ח.פ כבר רשום בחשבון פעמיים. ניתן עד להקים עד 2 עסקים עם אותו מספר עוסק. |
| 2114 | מספר תיק ניכויים אינו תקין. |
| 2115 | אחוז ניכוי במקור אינו תקין. ערך תקין הוא מספר בין 0-35. |
| 2116 | ערך שיטת דיווח לא תקין. |
| 2117 | ניתן להוסיף עד 3 כתובות מייל להנהלת חשבונות. |
| 2118 | חלק מההשדות לא עודכנו. קיים עסק נוסף עם מספר עוסק זהה ולכן חייב להישמר ביניהם טווח הפרש של לפחות 8,000. |
| 2119 | מספור מסמך לא תקין. ערכים תקינים בין 1-999999999. |
| 2120 | שדה {types} לא נשלח. |
| 2121 | לא ניתן לעדכן מספור זה מאחר וכבר הופקו מסמכים בשנה זו. |
| 2122 | לא ניתן לבצע פעולה זו בעסק מוקפא. |
| 2123 | ערך {id} לא תקין של העסק |
| 2124 | תוכן בתחתית המסמך מוגבל ל-2000 תווים. |
| 2200 | ניתן להוסיף עד 3 כתובות מייל ללקוח. |
| 2201 | נא למלא שם לקוח. |
| 2202 | לא ניתן לאחד לקוח פעיל. |
| 2203 | לא ניתן למחוק לקוח שהופקו עבורו מסמכים. |
| 2204 | שדה {id} של לקוח מטרה לא נשלח. |
| 2205 | לא נמצאו לקוחות חדשים או שהקובץ המיובא אינו תקין. |
| 2206 | ניתן להוסיף עד 3 תגיות ללקוח. |
| 2207 | קובץ לא תקין או גדול מ 5M. |
| 2208 | יתרה לא תקינה. |
| 2209 | הכנסות לא תקינות. |
| 2210 | לא ניתן למחוק לקוח בעל כרטיסי אשראי שמורים. |
| 2250 | ניתן להוסיף עד 3 כתובות מייל לספק. |
| 2251 | נא למלא שם ספק. |
| 2252 | לא ניתן לאחד ספק פעיל. |
| 2253 | לא ניתן למחוק ספק ששויכו אליו הוצאות. |
| 2254 | שדה {id} של ספק מטרה לא נשלח. |
| 2255 | לא נמצאו ספקים חדשים ותקינים בקובץ היבוא. |
| 2256 | ניתן להוסיף עד 3 תגיות ללקוח. |
| 2257 | קובץ לא תקין או גדול מ 5M. |
| 2258 | יתרה לא תקינה. |
| 2259 | הכנסות לא תקינות. |
| 2300 | נא למלא שם פריט. |
| 2301 | נא למלא תיאור פריט. |
| 2302 | לא נמצאו פריטים חדשים ותקינים בקובץ היבוא. |
| 2305 | קובץ לא תקין או גדול מ 5M. |
| 2400 | לא ניתן לסגור מסמך שאינו פתוח. |
| 2401 | לא ניתן לפתוח מסמך שאינו סגור ידנית. |
| 2402 | שדה {ids} לא נשלח או לא תקין. |
| 2403 | סוג מסמך לא נשלח או אינו נתמך עבור סוג עסק זה. |
| 2404 | Invalid or missing {linkType} field. Can be only (copy|cancel|link). |
| 2405 | התאריך שנבחר עתידי או מוקדם מדי לסוג מסמך זה. |
| 2406 | ערך שפה לא תקין. |
| 2407 | ערך קוד מטבע לא תקין. |
| 2408 | תאריך לתשלום עד לא תקין. |
| 2409 | סוג מע"מ לא תקין. |
| 2410 | שדה לקוח {client} חסר. |
| 2411 | לקוח לא קיים. |
| 2412 | חשבונית עצמית יכולה להיות מופקת רק עם סוג חשבונית מס. |
| 2413 | נא למלא לפחות שירות או פריט אחד. |
| 2414 | סכום תשלום לא תקין. צריך להיות מספר עשרוני. |
| 2415 | תיאור שורה לא יכול להיות ריק. |
| 2416 | סכום מסמך לא תקין. צריך להיות שונה מאפס. |
| 2417 | סכום מסמך לא תקין. צריך להיות גדול מאפס. |
| 2418 | סכום מסמך לא תקין. צריך להיות גדול או שווה לאפס. |
| 2419 | נא למלא לפחות שורת תקבולים אחת. |
| 2420 | Invalid discount type. Can be 'sum' or 'percentage'. |
| 2421 | קוד סוג תשלום לא תקין. |
| 2422 | קיים חוסר התאמה בין סכום התקבולים לסכום התשלומים. |
| 2423 | סוג כרטיס אשראי לא תקין. |
| 2424 | קוד סוג עסקה לא תקין. |
| 2425 | מספר תשלומים יכול להיות רק 1-36. |
| 2426 | תאריך תקבול ריק, עתידי או לא תקין. |
| 2427 | לא ניתן לשלוח במייל מסמך שלא נחתם דיגיטלית. |
| 2428 | נא למלא שורת תקבולים אחת לפחות בנוסף לניכוי במקור. |
| 2429 | מסמך מקושר לא נמצא. |
| 2430 | ערך כמות צריך להיות גדול מ 1. |
| 2431 | כמות מירבית מותרת של שורות הכנסה / תשלום היא 200 למסמך. |
| 2432 | סוג עותק מסמך לא נתמך. |
| 2433 | סוג סטטוס הפצת מייל לא נתמך. |
| 2434 | ערך סכום תקבול צריך להיות שונה מ 0. |
| 2435 | ערך טקסט הערות לא תקין. |
| 2436 | ערך טקסט תחתון לא תקין. |
| 2437 | ערך שליחת מסמך במייל לא תקין. |
| 2500 | כתובת לא תקינה. |
| 2501 | קטגוריה חסרה. |
| 2502 | כותרת חסרה. |
| 2503 | כתובת חסרה. |
| 2504 | רשימת מיון ריקה. |
| 2600 | לא נמצא מסוף סליקה פעיל. |
| 2601 | קיימת בעיה בחיוב אשראי, נא ליצור קשר עם התמיכה. |
| 2602 | שגיאה בחיבור תוסף. |
| 2603 | שגיאה בחיוב כרטיס אשראי. |
| 2604 | ערך flow לא תקין. |
| 2605 | לא נשלח תוכן מסמך. |
| 2606 | שגיאה בשינוי סטטוס מסוף. |
| 2607 | סוג טוקן לא תקין. |
| 2608 | 4 ספרות של כרטיס אשראי אינם תקינים. |
| 2609 | סוג מזהה עסקה לא תקין. |
| 2610 | סכום תשלום לא תקין. צריך להיות גדול מאפס. |
| 2611 | שגיאת אשראי. |
| 2612 | מזהה עסקה לא תקין. |
| 2613 | סוג סטטוס עסקה לא תקין. |
| 2614 | שדה מותאם אישית לא תקין. |
| 2615 | לא ניתן לבטל עסקה שבוטלה. |
| 2616 | לא ניתן לבטל עסקה, נא לבצע זיכוי. |
| 2617 | לא ניתן לזכות עסקה. |
| 2618 | לא ניתן לבטל עסקה שבוטלה. |
| 2619 | שדה סוג חיוב לא תקין |
| 2620 | בקשה הושלמה בעבר. |
| 2621 | לא ניתן לבטל או לזכות עסקה. |
| 2622 | שם בעל כרטיס לא תקין. |
| 2623 | תוקף כרטיס לא תקין. |
| 2624 | לא ניתן לזכות עסקה בסכום גדול מהסכום המקורי. |
| 2625 | לתוסף שנבחר אין הרשאה לשמירת כרטיסי אשראי. |
| 2626 | שם משלם לא תקין. |
| 2627 | כרטיס אשראי שמור לא קיים או לא פעיל. |
| 2700 | מפתח API לא תקין. |
| 2701 | מצב מפתח API לא תקין. |
| 2702 | סוג מפתח דורש הזדהות נוספת. |
| 2800 | קוד חשבון ריק. |
| 2801 | סוג ממשק לא ניתן לסנכרון. |
| 2802 | סוג ממשק חיצוני לא תקין. |
| 2803 | שגיאת התחברות לממשק חיצוני. |
| 2804 | שגיאת תוסף. |
| 2805 | תוסף לא פעיל. |
| 2900 | תאריך התחלה לא תקין. |
| 2901 | תאריך סיום לא תקין או שאינו מאפשר לפחות הפקת מסמך אחד. |
| 2902 | תקופת חזרה לא תקינה. |
| 2903 | סטטוס ריטיינר לא תקין. |
| 2904 | תאריך ריטיינר לא תקין. |
| 3000 | שגיאה כללית. |
| 3001 | לא קיים כרטיס אשראי בחשבון. |
| 3002 | סוג המינוי שנשלח לא קיים. |
| 4000 | סוג נתונים לא תקין. |
| 3003 | סוג פעולה לא נתמך. |
| 3004 | שדה אחד או יותר חסרים. |
| 3005 | מינוי זהה קיים בחשבון. |
| 3006 | מכסת ההרשמות היומית הסתיימה. נסו שוב מחר או פנו למנהל תיק הלקוח שלכם להגדלת המכסה היומית. |
| 3007 | מכסת החיבורים היומית הסתיימה. נסו שוב מחר או פנו למנהל תיק הלקוח שלכם להגדלת המכסה היומית. |
| 3008 | לא ניתן להפעיל את החיבור. |
| 3009 | סוג טרנזאקציה לא נתמכת. |
| 3010 | קיים חוב בחשבון. נא להסדיר את החוב לפני רכישת מינוי חדש. |
| 3100 | שם תגית ריק. |
| 3101 | אורך מקסימלי של תגית אפשרי עד 30 תווים. |
| 3200 | סוג משימה לא נתמך. |
| 3300 | סוג סטטוס הוצאה לא נתמך. |
| 3301 | סכום הוצאה לא תקין. |
| 3302 | סכום מע״מ בהוצאה לא תקין. |
| 3303 | נא לצרף קובץ עבור ההוצאה. |
| 3304 | סוג טיוטת הוצאה לא נתמך. |
| 3305 | טיוטת הוצאה מקושרת לא נמצאה. |
| 3306 | מספר מסמך הוצאה לא תקין. |
| 3307 | תאריך מסמך הוצאה לא תקין. |
| 3308 | סוג מסמך הוצאה לא תקין. |
| 3309 | לא ניתן לסווג מסמכי הכנסה של העסק כהוצאה. |
| 3310 | חודש דיווח לא תקין. |
| 3311 | נא למלא פרטי ספק. |
| 3312 | נא למלא פרטי סוג הוצאה. |
| 3313 | שדה expenseIds לא תקין. |
| 3314 | לא ניתן לעדכן הוצאה לאחר שדווחה. |
| 3315 | לא ניתן לפתוח הוצאה שלא דווחה. |
| 3316 | לא ניתן לסגור הוצאה שאינה פתוחה. |
| 3317 | סוג אמצעי התשלום של ההוצאה לא תקין. |
| 3318 | מיקום משרד לא תקין. |
| 3319 | מספר חדרים לא תקין. |
| 3320 | מספר רכב לא תקין. |
| 3400 | נא למלא כותרת לחשבון. |
| 3401 | שיעור הוצאה מוכרת לא תקין. |
| 3402 | שיעור מע״מ מוכר לא תקין. |
| 3403 | סוג ההוצאה לא תקין. |
| 3404 | קוד 6111 לא תקין. |
| 3405 | לא ניתן למחוק סוג הוצאה ששויכו אליו הוצאות. |

MCP Server · Soon

# Bring your morning data into _your AI assistant._

Soon, Claude Code, Cursor and VS Code will answer questions about your documents, clients and expenses in plain language, on your own API key.

[Explore the API](https://developers.morning.co/api) [Get your API keys](https://app.greeninvoice.co.il/settings/developers/api)

Your API key Sandbox included

Coming to ![](https://developers.morning.co/logos/claude-code.svg)Claude Code ![](https://developers.morning.co/logos/cursor.svg)Cursor ![](https://developers.morning.co/logos/vscode.svg)VS Code

![](https://developers.morning.co/logos/claude-code.svg)claude — ~/studio-ofek

Coming soon

## What's coming

### Ask in plain language

"Which invoices from last month are still open?" — answered from your own business data, right where you work.

### Your documents, clients and expenses

Look up the records you work with every day — without leaving your editor or switching tabs.

### On your own API key

No new credentials to manage — it runs on the API keys you already create in Developer Tools.

Works where you work

## Your assistant, your editor

![](https://developers.morning.co/logos/claude-code.svg)

### Claude Code

Ask about your invoices without leaving the terminal — one command to connect.

![](https://developers.morning.co/logos/cursor.svg)

### Cursor

Your business data in the editor's chat, next to the code that uses it.

![](https://developers.morning.co/logos/vscode.svg)

### VS Code

Look up documents, clients and expenses from chat in agent mode.

### And more

Any MCP client that can connect to a remote server with your API key.

Setup guides for each client arrive with the launch.

## FAQ

Something missing? Visit the [morning help center](https://support.greeninvoice.co.il).

What is MCP?

The [Model Context Protocol](https://modelcontextprotocol.io) (MCP) is an open standard that lets AI assistants connect to outside tools and data. With the morning MCP server, your assistant will be able to look up your documents, clients and expenses and answer questions about them.

Which AI tools will it work with?

At launch: Claude Code, Cursor and VS Code — any MCP client that can send an API key with its requests.

Can I start building now?

Yes — the [REST API](https://developers.morning.co/api) is live today, and the API key you create for it is the one the MCP server will use.

## Can't wait?

The REST API is live today — documents, payments, webhooks and more.

[Open the API Documentation →](https://developers.morning.co/api)

404

# Page not found

The page you’re looking for doesn’t exist. It may have been moved, or the address may be mistyped.

[Back to the documentation](https://developers.morning.co/)