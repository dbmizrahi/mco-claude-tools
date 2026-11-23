/** Parameter building blocks shared by the section files. */
import { z } from "zod";

/** No parameters (unknown keys are rejected). */
export const none = z.strictObject({});

/** Safe for a URL path segment. */
export const pathId = z.string().regex(/^[0-9A-Za-z_.@-]{1,64}$/, "letters, digits and - _ . @ only");
/** A PBX extension, e.g. "100". */
export const extension = z.string().regex(/^[0-9]{3,4}$/, "a PBX extension such as 100");
/** A phone number in international format; "+" is optional. */
export const phone = z.string().regex(/^\+?[0-9]{5,16}$/, "a phone number in international format, digits only");
export const positiveInt = z.number().int().positive();
export const dateTime = z
  .string()
  .regex(/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/, "format YYYY-MM-DD HH:MM:SS");
export const onOff = z.enum(["on", "off"]);
export const language = z.enum(["en", "es", "de", "pl", "ru", "ua", "fr"]);
/** Local audio file to upload (MP3 or WAV, up to 5 MB, absolute path). */
export const audioFilePath = z.string().min(1).describe("absolute path of a local MP3 or WAV file, up to 5 MB");

export const skipLimit = {
  skip: z.number().int().min(0).optional(),
  limit: z.number().int().min(1).max(1000).optional(),
};
export const takeSkip = {
  take: z.number().int().min(1).max(1000).optional(),
  skip: z.number().int().min(0).optional(),
};
