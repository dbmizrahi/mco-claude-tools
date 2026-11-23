/**
 * Teamsale CRM: customers (with source tags, labels, custom properties,
 * timeline and employees), leads, users, contacts, deals (with feed), tasks,
 * calls and files. API reference section "Teamsale CRM methods".
 * Nested objects are sent as form fields (`customer[name]=...`), like the
 * official Zadarma clients. File attachments on feed notes are not supported.
 */
import { z } from "zod";

import { dateTime, none, positiveInt, takeSkip } from "./common.js";
import { defineAction, defineTool, type ToolDef } from "./define.js";

const employeesCount = z.enum(["50", "50_250", "250_500"]);
const leadSource = z.enum(["manual", "call_incoming", "call_outgoing", "form"]);
const phones = z.array(z.strictObject({ type: z.enum(["work", "personal"]), phone: z.string().min(3) }));
const contacts = z.array(
  z.strictObject({
    type: z.enum(["email_work", "email_personal", "skype", "telegram", "viber", "whatsapp"]),
    value: z.string().min(1),
  }),
);
const idRefs = z.array(z.strictObject({ id: positiveInt }));
const customProperties = z.array(
  z.strictObject({ id: positiveInt.optional(), key: z.string().optional(), value: z.string() }),
);
const sortDesc = z.union([z.literal(0), z.literal(1)]);

const partyFields = {
  responsible_user_id: positiveInt.optional(),
  employees_count: employeesCount.optional(),
  comment: z.string().optional(),
  country: z.string().regex(/^[A-Za-z]{2}$/, "two-letter country code").optional(),
  city: z.string().optional(),
  address: z.string().optional(),
  zip: z.string().optional(),
  website: z.string().optional(),
  lead_source: leadSource.optional(),
  phones: phones.optional(),
  contacts: contacts.optional(),
  labels: idRefs.optional(),
  utms: idRefs.optional(),
  custom_properties: customProperties.optional(),
};

const customerData = z.strictObject({
  name: z.string().min(1).optional(),
  status: z.enum(["individual", "company"]).optional(),
  type: z.enum(["potential", "client", "reseller", "partner"]).optional(),
  ...partyFields,
});

const utmData = z.strictObject({
  param: z.enum(["utm_source", "utm_medium", "utm_campaign", "utm_content", "phone", "custom"]),
  value: z.string().min(1),
  display_value: z.string().optional(),
});

const employeeData = z.strictObject({
  name: z.string().min(1).optional(),
  position: z.enum(["ceo", "director", "manager", "sales_manager", "hr", "support", "custom"]).optional(),
  position_title: z.string().optional(),
  comment: z.string().optional(),
  phones: phones.optional(),
  contacts: contacts.optional(),
});

const customerId = { customer_id: positiveInt };
const listHint = "use search, filter or take/skip";

export const crmCustomersTool: ToolDef = defineTool(
  "zadarma_crm_customers",
  "Teamsale CRM customers",
  "Teamsale CRM customers (clients) and their source tags, labels, custom properties, timeline notes and employees.",
  [
    defineAction("list", {
      description: "List customers with search, filter, sort and paging (take default 20).",
      method: "GET",
      path: "/v1/zcrm/customers",
      params: z.strictObject({
        search: z.string().optional(),
        filter: z
          .strictObject({
            status: z.enum(["individual", "company"]).optional(),
            type: z.enum(["potential", "client", "reseller", "partner"]).optional(),
            country: z.string().optional(),
            city: z.string().optional(),
            label: positiveInt.optional(),
            utm: positiveInt.optional(),
            employees_count: employeesCount.optional(),
            responsible: positiveInt.optional(),
          })
          .optional(),
        sort: z.strictObject({ attr: z.enum(["name", "status", "type"]), desc: sortDesc }).optional(),
        ...takeSkip,
      }),
      kind: "read",
      narrowHint: listHint,
    }),
    defineAction("get", {
      description: "One customer by ID, with phones, contacts, labels, tags and custom properties.",
      method: "GET",
      path: "/v1/zcrm/customers/{customer_id}",
      params: z.strictObject(customerId),
      kind: "read",
    }),
    defineAction("create", {
      description: "Create a customer. labels/utms take existing IDs.",
      method: "POST",
      path: "/v1/zcrm/customers",
      params: z.strictObject({ customer: customerData.extend({ name: z.string().min(1) }) }),
      kind: "write",
    }),
    defineAction("update", {
      description: "Update a customer; only the given fields change.",
      method: "PUT",
      path: "/v1/zcrm/customers/{customer_id}",
      params: z.strictObject({ ...customerId, customer: customerData }),
      kind: "write",
    }),
    defineAction("delete", {
      description: "Delete a customer.",
      method: "DELETE",
      path: "/v1/zcrm/customers/{customer_id}",
      params: z.strictObject(customerId),
      kind: "dangerous",
      risk: "deletes the customer from the CRM; this cannot be undone",
    }),
    defineAction("utms_list", {
      description: "All source tags (UTM, phone, custom) with statistics.",
      method: "GET",
      path: "/v1/zcrm/customers/utms",
      params: none,
      kind: "read",
    }),
    defineAction("utm_create", {
      description: "Create a source tag.",
      method: "POST",
      path: "/v1/zcrm/customers/utms",
      params: z.strictObject({ utm: utmData }),
      kind: "write",
    }),
    defineAction("utm_update", {
      description: "Update a source tag.",
      method: "PUT",
      path: "/v1/zcrm/customers/utms/{utm_id}",
      params: z.strictObject({ utm_id: positiveInt, utm: utmData }),
      kind: "write",
    }),
    defineAction("utm_delete", {
      description: "Delete a source tag.",
      method: "DELETE",
      path: "/v1/zcrm/customers/utms/{utm_id}",
      params: z.strictObject({ utm_id: positiveInt }),
      kind: "dangerous",
      risk: "deletes the source tag; this cannot be undone",
    }),
    defineAction("labels_list", {
      description: "All labels with statistics.",
      method: "GET",
      path: "/v1/zcrm/customers/labels",
      params: none,
      kind: "read",
    }),
    defineAction("label_create", {
      description: "Create a label.",
      method: "POST",
      path: "/v1/zcrm/customers/labels",
      params: z.strictObject({ name: z.string().min(1) }),
      kind: "write",
    }),
    defineAction("label_delete", {
      description: "Delete a label.",
      method: "DELETE",
      path: "/v1/zcrm/customers/labels/{label_id}",
      params: z.strictObject({ label_id: positiveInt }),
      kind: "dangerous",
      risk: "deletes the label from all customers; this cannot be undone",
    }),
    defineAction("custom_properties", {
      description: "Custom properties (additional fields) defined for customers.",
      method: "GET",
      path: "/v1/zcrm/customers/custom-properties",
      params: none,
      kind: "read",
    }),
    defineAction("feed_list", {
      description: "Timeline records of a customer.",
      method: "GET",
      path: "/v1/zcrm/customers/{customer_id}/feed",
      params: z.strictObject(customerId),
      kind: "read",
    }),
    defineAction("feed_add", {
      description: "Add a text note to a customer's timeline.",
      method: "POST",
      path: "/v1/zcrm/customers/{customer_id}/feed",
      params: z.strictObject({ ...customerId, content: z.string().min(1) }),
      kind: "write",
    }),
    defineAction("feed_update", {
      description: "Change the text of a timeline note.",
      method: "PUT",
      path: "/v1/zcrm/customers/{customer_id}/feed/{item_id}",
      params: z.strictObject({ ...customerId, item_id: positiveInt, content: z.string().min(1) }),
      kind: "write",
    }),
    defineAction("feed_delete", {
      description: "Delete a timeline note.",
      method: "DELETE",
      path: "/v1/zcrm/customers/{customer_id}/feed/{item_id}",
      params: z.strictObject({ ...customerId, item_id: positiveInt }),
      kind: "dangerous",
      risk: "deletes the note; this cannot be undone",
    }),
    defineAction("employees_list", {
      description: "Employees of a customer.",
      method: "GET",
      path: "/v1/zcrm/customers/{customer_id}/employees",
      params: z.strictObject(customerId),
      kind: "read",
    }),
    defineAction("employee_get", {
      description: "One employee of a customer.",
      method: "GET",
      path: "/v1/zcrm/customers/{customer_id}/employees/{employee_id}",
      params: z.strictObject({ ...customerId, employee_id: positiveInt }),
      kind: "read",
    }),
    defineAction("employee_create", {
      description: "Add an employee to a customer (position_title for position custom).",
      method: "POST",
      path: "/v1/zcrm/customers/{customer_id}/employees",
      params: z.strictObject({ ...customerId, employee: employeeData.extend({ name: z.string().min(1) }) }),
      kind: "write",
    }),
    defineAction("employee_update", {
      description: "Update an employee of a customer.",
      method: "PUT",
      path: "/v1/zcrm/customers/{customer_id}/employees/{employee_id}",
      params: z.strictObject({ ...customerId, employee_id: positiveInt, employee: employeeData }),
      kind: "write",
    }),
    defineAction("employee_delete", {
      description: "Delete an employee of a customer.",
      method: "DELETE",
      path: "/v1/zcrm/customers/{customer_id}/employees/{employee_id}",
      params: z.strictObject({ ...customerId, employee_id: positiveInt }),
      kind: "dangerous",
      risk: "deletes the employee record; this cannot be undone",
    }),
  ],
);

const leadData = z.strictObject({
  name: z.string().min(1).optional(),
  lead_status: z.enum(["not_processed", "in_progress", "finished"]).optional(),
  ...partyFields,
});
const convert = z.union([z.literal(0), z.literal(1), z.literal(2)]).describe("0 keep as lead, 1 convert to client, 2 poor (delete)");

export const crmLeadsTool: ToolDef = defineTool(
  "zadarma_crm_leads",
  "Teamsale CRM leads",
  "Teamsale CRM leads: list, get, create, update (and convert to a client), delete.",
  [
    defineAction("list", {
      description:
        "List leads. filter.responsible: a user ID, or the string \"null\" (assigned), \"-1\" (unassigned), \"-2\" (all).",
      method: "GET",
      path: "/v1/zcrm/leads",
      params: z.strictObject({
        search: z.string().optional(),
        filter: z
          .strictObject({
            source: leadSource.optional(),
            responsible: z.string().optional(),
            label: positiveInt.optional(),
            utm: positiveInt.optional(),
            createdAfter: dateTime.optional(),
            createdBefore: dateTime.optional(),
          })
          .optional(),
        sort: z
          .strictObject({
            attr: z.enum(["name", "lead_source", "lead_status", "responsible_user_id", "lead_created_at"]),
            desc: sortDesc,
          })
          .optional(),
        ...takeSkip,
      }),
      kind: "read",
      narrowHint: listHint,
    }),
    defineAction("get", {
      description: "One lead by ID.",
      method: "GET",
      path: "/v1/zcrm/leads/{lead_id}",
      params: z.strictObject({ lead_id: positiveInt }),
      kind: "read",
    }),
    defineAction("create", {
      description: "Create a lead (convert 0), or create it directly as a client (convert 1).",
      method: "POST",
      path: "/v1/zcrm/leads",
      params: z.strictObject({ convert, lead: leadData.extend({ name: z.string().min(1) }) }),
      kind: "write",
    }),
    defineAction("update", {
      description: "Update a lead; convert 1 turns it into a client, convert 2 marks it poor and deletes it.",
      method: "PUT",
      path: "/v1/zcrm/leads/{lead_id}",
      params: z.strictObject({ lead_id: positiveInt, convert: convert.optional(), lead: leadData }),
      kind: "write",
      dangerousWhen: (args) => args.convert === 2,
      risk: "convert 2 deletes the lead; this cannot be undone",
    }),
    defineAction("delete", {
      description: "Delete a lead.",
      method: "DELETE",
      path: "/v1/zcrm/leads/{lead_id}",
      params: z.strictObject({ lead_id: positiveInt }),
      kind: "dangerous",
      risk: "deletes the lead; this cannot be undone",
    }),
  ],
);

export const crmUsersTool: ToolDef = defineTool(
  "zadarma_crm_users",
  "Teamsale CRM users",
  "Teamsale CRM users (your team): list, one user, working hours, groups and rights.",
  [
    defineAction("list", { description: "List users.", method: "GET", path: "/v1/zcrm/users", params: none, kind: "read" }),
    defineAction("get", {
      description: "One user by ID.",
      method: "GET",
      path: "/v1/zcrm/users/{user_id}",
      params: z.strictObject({ user_id: positiveInt }),
      kind: "read",
    }),
    defineAction("working_hours", {
      description: "Working hours of a user.",
      method: "GET",
      path: "/v1/zcrm/users/{user_id}/working-hours",
      params: z.strictObject({ user_id: positiveInt }),
      kind: "read",
    }),
    defineAction("groups", {
      description: "User groups and the rights in each.",
      method: "GET",
      path: "/v1/zcrm/users/groups",
      params: none,
      kind: "read",
    }),
  ],
);

export const crmContactsTool: ToolDef = defineTool(
  "zadarma_crm_contacts",
  "Teamsale CRM contacts",
  "All CRM contacts with phone numbers (clients, employees, leads, users): search, and identify a phone number.",
  [
    defineAction("list", {
      description: "List contacts; search by name, phone or extension.",
      method: "GET",
      path: "/v1/zcrm/contacts",
      params: z.strictObject({ search: z.string().optional(), ...takeSkip }),
      kind: "read",
      narrowHint: listHint,
    }),
    defineAction("identify", {
      description: "Find who a phone number belongs to.",
      method: "GET",
      path: "/v1/zcrm/contacts/identify",
      params: z.strictObject({ phone: z.string().min(3) }),
      kind: "read",
    }),
  ],
);

const dealStatus = z.enum(["new", "in_progress", "decision", "payment", "success", "canceled"]);
const dealFields = {
  title: z.string().min(1).optional(),
  budget: z.number().min(0).optional(),
  currency: z.string().regex(/^[A-Z]{3}$/, "ISO 4217 code such as USD").optional(),
  status: dealStatus.optional(),
  responsible_user: positiveInt.optional(),
};
const dealId = { deal_id: positiveInt };

export const crmDealsTool: ToolDef = defineTool(
  "zadarma_crm_deals",
  "Teamsale CRM deals",
  "Teamsale CRM deals and their feed notes.",
  [
    defineAction("list", {
      description: "List deals; search by title; filter by currency, responsible_user, status.",
      method: "GET",
      path: "/v1/zcrm/deals",
      params: z.strictObject({
        search: z.string().optional(),
        filter: z
          .strictObject({ currency: z.string().optional(), responsible_user: positiveInt.optional(), status: dealStatus.optional() })
          .optional(),
        sort: z.strictObject({ attr: z.enum(["title", "budget", "status", "created_at"]), desc: sortDesc }).optional(),
        ...takeSkip,
      }),
      kind: "read",
      narrowHint: listHint,
    }),
    defineAction("get", {
      description: "One deal by ID.",
      method: "GET",
      path: "/v1/zcrm/deals/{deal_id}",
      params: z.strictObject(dealId),
      kind: "read",
    }),
    defineAction("create", {
      description: "Create a deal, optionally linked to a customer.",
      method: "POST",
      path: "/v1/zcrm/deals",
      params: z.strictObject({
        deal: z.strictObject({ ...dealFields, title: z.string().min(1), customer_id: positiveInt.optional() }),
      }),
      kind: "write",
    }),
    defineAction("update", {
      description: "Update a deal; only the given fields change.",
      method: "PUT",
      path: "/v1/zcrm/deals/{deal_id}",
      params: z.strictObject({ ...dealId, deal: z.strictObject(dealFields) }),
      kind: "write",
    }),
    defineAction("delete", {
      description: "Delete a deal.",
      method: "DELETE",
      path: "/v1/zcrm/deals/{deal_id}",
      params: z.strictObject(dealId),
      kind: "dangerous",
      risk: "deletes the deal; this cannot be undone",
    }),
    defineAction("feed_list", {
      description: "Feed records of a deal.",
      method: "GET",
      path: "/v1/zcrm/deals/{deal_id}/feed",
      params: z.strictObject(dealId),
      kind: "read",
    }),
    defineAction("feed_add", {
      description: "Add a text note to a deal's feed.",
      method: "POST",
      path: "/v1/zcrm/deals/{deal_id}/feed",
      params: z.strictObject({ ...dealId, content: z.string().min(1) }),
      kind: "write",
    }),
    defineAction("feed_update", {
      description: "Change the text of a deal feed note.",
      method: "PUT",
      path: "/v1/zcrm/deals/{deal_id}/feed/{item_id}",
      params: z.strictObject({ ...dealId, item_id: positiveInt, content: z.string().min(1) }),
      kind: "write",
    }),
    defineAction("feed_delete", {
      description: "Delete a deal feed note.",
      method: "DELETE",
      path: "/v1/zcrm/deals/{deal_id}/feed/{item_id}",
      params: z.strictObject({ ...dealId, item_id: positiveInt }),
      kind: "dangerous",
      risk: "deletes the note; this cannot be undone",
    }),
  ],
);

const eventFields = {
  title: z.string().min(1).optional(),
  description: z.string().optional().describe("Quill Delta JSON"),
  start: dateTime.optional(),
  end: dateTime.optional(),
  allDay: z.boolean().optional(),
  responsible_user: positiveInt.optional(),
  phone: z.string().optional(),
  members: z.array(positiveInt).optional(),
  customers: z.array(positiveInt).optional(),
};
const eventId = { event_id: positiveInt };

export const crmTasksTool: ToolDef = defineTool(
  "zadarma_crm_tasks",
  "Teamsale CRM tasks",
  "Teamsale CRM tasks and planned calls (events): list, get, create, update, close, delete.",
  [
    defineAction("list", {
      description: "List tasks; filter.completed 1 also shows completed tasks.",
      method: "GET",
      path: "/v1/zcrm/events",
      params: z.strictObject({
        search: z.string().optional(),
        filter: z
          .strictObject({
            responsible: positiveInt.optional(),
            createdBy: positiveInt.optional(),
            start: dateTime.optional(),
            end: dateTime.optional(),
            completed: z.union([z.literal(0), z.literal(1)]).optional(),
          })
          .optional(),
        sort: z.strictObject({ attr: z.enum(["responsible", "title", "start", "end"]), desc: sortDesc }).optional(),
        ...takeSkip,
      }),
      kind: "read",
      narrowHint: listHint,
    }),
    defineAction("get", {
      description: "One task by ID.",
      method: "GET",
      path: "/v1/zcrm/events/{event_id}",
      params: z.strictObject(eventId),
      kind: "read",
    }),
    defineAction("create", {
      description: "Create a task (type task) or a planned call (type call, with phone).",
      method: "POST",
      path: "/v1/zcrm/events",
      params: z.strictObject({
        event: z.strictObject({ type: z.enum(["task", "call"]).optional(), ...eventFields, title: z.string().min(1) }),
      }),
      kind: "write",
    }),
    defineAction("update", {
      description: "Update a task; only the given fields change.",
      method: "PUT",
      path: "/v1/zcrm/events/{event_id}",
      params: z.strictObject({ ...eventId, event: z.strictObject(eventFields) }),
      kind: "write",
    }),
    defineAction("close", {
      description: "Mark a task as completed, with an optional comment.",
      method: "POST",
      path: "/v1/zcrm/events/{event_id}/close",
      params: z.strictObject({ ...eventId, comment: z.string().optional() }),
      kind: "write",
    }),
    defineAction("delete", {
      description: "Delete a task.",
      method: "DELETE",
      path: "/v1/zcrm/events/{event_id}",
      params: z.strictObject(eventId),
      kind: "dangerous",
      risk: "deletes the task; this cannot be undone",
    }),
  ],
);

export const crmCallsFilesTool: ToolDef = defineTool(
  "zadarma_crm_calls_files",
  "Teamsale CRM calls and files",
  "Teamsale CRM call list, and file information by ID (metadata only; file contents are never returned).",
  [
    defineAction("calls_list", {
      description: "List CRM calls; filter by user, type incoming|outgoing, status, dateFrom/dateTo.",
      method: "GET",
      path: "/v1/zcrm/calls",
      params: z.strictObject({
        search: z.string().optional(),
        filter: z
          .strictObject({
            user: positiveInt.optional(),
            type: z.enum(["incoming", "outgoing"]).optional(),
            status: z.enum(["answer", "noanswer", "cancel", "busy", "failed"]).optional(),
            dateFrom: dateTime.optional(),
            dateTo: dateTime.optional(),
          })
          .optional(),
        sort: z.strictObject({ attr: z.enum(["phone", "status", "duration", "time"]), desc: sortDesc }).optional(),
        ...takeSkip,
      }),
      kind: "read",
      narrowHint: listHint,
    }),
    defineAction("file_get", {
      description: "Information about a CRM file by ID (type and size; contents are not returned).",
      method: "GET",
      path: "/v1/zcrm/files/{file_id}",
      params: z.strictObject({ file_id: positiveInt }),
      kind: "read",
    }),
  ],
);
