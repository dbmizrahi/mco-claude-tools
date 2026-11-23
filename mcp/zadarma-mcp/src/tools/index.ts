/** All Zadarma tools, in the order they are listed to the client. */
import { crmCallsFilesTool, crmContactsTool, crmCustomersTool, crmDealsTool, crmLeadsTool, crmTasksTool, crmUsersTool } from "./crm.js";
import type { ToolDef } from "./define.js";
import { ivrMenusTool, ivrScenariosTool, ivrSoundsTool } from "./ivr.js";
import { pbxExtLinesTool, pbxExtensionsTool, pbxHoldMusicTool, pbxRecordsTool, pbxTool } from "./pbx.js";
import { esimTool, numbersTool, smsTool, speechTool, verifyTool, webrtcTool } from "./services.js";
import { callbackTool, infoTool, sipTool, statisticsTool, tariffTool } from "./telephony.js";

export const ALL_TOOLS: readonly ToolDef[] = [
  infoTool,
  callbackTool,
  sipTool,
  tariffTool,
  statisticsTool,
  pbxTool,
  pbxExtensionsTool,
  pbxExtLinesTool,
  pbxRecordsTool,
  pbxHoldMusicTool,
  ivrSoundsTool,
  ivrMenusTool,
  ivrScenariosTool,
  speechTool,
  numbersTool,
  smsTool,
  webrtcTool,
  esimTool,
  verifyTool,
  crmCustomersTool,
  crmLeadsTool,
  crmUsersTool,
  crmContactsTool,
  crmDealsTool,
  crmTasksTool,
  crmCallsFilesTool,
];
