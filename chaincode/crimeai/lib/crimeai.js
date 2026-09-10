'use strict';

const { Contract } = require('fabric-contract-api');

class CrimeAIContract extends Contract {

    async CreateAudit(
        ctx,
        caseId,
        action,
        performedBy,
        timestamp,
        dataHash
    ) {
        const transactionId = ctx.stub.getTxID();

        const auditRecord = {
            caseId: caseId,
            action: action,
            performedBy: performedBy,
            timestamp: timestamp,
            dataHash: dataHash,
            transactionId: transactionId
        };

        const existingData = await ctx.stub.getState(caseId);

        let audits = [];

        if (existingData && existingData.length > 0) {
            audits = JSON.parse(existingData.toString());
        }

        audits.push(auditRecord);

        await ctx.stub.putState(
            caseId,
            Buffer.from(JSON.stringify(audits))
        );

        return Buffer.from(JSON.stringify(auditRecord));
    }

    async GetCaseAudits(ctx, caseId) {

        const data = await ctx.stub.getState(caseId);

        if (!data || data.length === 0) {
            return Buffer.from(JSON.stringify([]));
        }

        return data;
    }
}

module.exports = CrimeAIContract;
