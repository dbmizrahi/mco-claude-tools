/**
 * Request schema for the SubQ Decisions API (POST /v1/systemone), per
 * https://docs.subq.ai/endpoints/decisions-api/ — the same limits are enforced
 * here, so a bad request is rejected locally instead of costing a round trip.
 */
import { z } from "zod";

export const MAX_QUESTIONS = 128;
export const MAX_QUESTION_NAME = 100;
export const CHOICE_MIN = 2;
export const CHOICE_MAX = 255;
export const SCORE_MIN = 2;
export const SCORE_MAX = 10;
export const MAX_IMAGES = 4;

const instructions = z.string().min(1).describe("The question, in plain words.");

export const noulQuestionSchema = z.object({
  type: z.literal("noul"),
  instructions: instructions.optional(),
  criteria: z
    .object({
      true: z.string().optional(),
      false: z.string().optional(),
    })
    .optional()
    .describe("What a yes and a no mean."),
});

export const choiceQuestionSchema = z.object({
  type: z.literal("choice"),
  instructions: instructions.optional(),
  criteria: z
    .record(z.string().min(1), z.string().nullable())
    .describe(`${CHOICE_MIN}-${CHOICE_MAX} options, each mapped to a description or null.`),
});

export const scoreQuestionSchema = z.object({
  type: z.literal("score"),
  instructions: instructions.optional(),
  criteria: z
    .array(z.string().min(1))
    .min(SCORE_MIN)
    .max(SCORE_MAX)
    .describe(`${SCORE_MIN}-${SCORE_MAX} level labels, lowest first.`),
});

export const questionSchema = z.discriminatedUnion("type", [
  noulQuestionSchema,
  choiceQuestionSchema,
  scoreQuestionSchema,
]);

export const imageSchema = z.object({
  mediaType: z.enum(["image/png", "image/jpeg", "image/webp"]),
  base64: z.string().min(1).describe("Raw file bytes as one line of base64, no data: prefix."),
});

const jsonState = z.union([
  z.string().min(1),
  z.record(z.string(), z.unknown()),
  z.array(z.unknown()),
]);

/** Raw shape, as the MCP SDK's registerTool expects for inputSchema. */
export const decideInputShape = {
  state: jsonState.describe("The content to judge: text, an object or an array."),
  questions: z
    .record(z.string().min(1).max(MAX_QUESTION_NAME), questionSchema)
    .describe(`1-${MAX_QUESTIONS} named questions; each name becomes a key in answers.`),
  images: z.array(imageSchema).max(MAX_IMAGES).optional().describe(`Up to ${MAX_IMAGES} images.`),
};

export const decideRequestSchema = z.object(decideInputShape);

export type NoulQuestion = z.infer<typeof noulQuestionSchema>;
export type ChoiceQuestion = z.infer<typeof choiceQuestionSchema>;
export type ScoreQuestion = z.infer<typeof scoreQuestionSchema>;
export type Question = z.infer<typeof questionSchema>;
export type DecideRequest = z.infer<typeof decideRequestSchema>;

/** Checks the zod schema cannot express on its own. Returns an error or null. */
export function checkLimits(request: DecideRequest): string | null {
  const names = Object.keys(request.questions);
  if (names.length < 1 || names.length > MAX_QUESTIONS) {
    return `request needs 1-${MAX_QUESTIONS} questions, got ${names.length}`;
  }
  for (const name of names) {
    const question = request.questions[name];
    if (question === undefined) {
      continue;
    }
    if (question.type === "noul" && question.instructions === undefined && question.criteria === undefined) {
      return `noul question '${name}' needs instructions or criteria`;
    }
    if (question.type === "choice") {
      const count = Object.keys(question.criteria).length;
      if (count < CHOICE_MIN || count > CHOICE_MAX) {
        return `choice question '${name}' needs ${CHOICE_MIN}-${CHOICE_MAX} options, got ${count}`;
      }
    }
  }
  return null;
}
