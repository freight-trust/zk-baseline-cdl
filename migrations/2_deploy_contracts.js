const ZeroKnowledgeIdentityIssueContract = artifacts.require(
  "ZeroKnowledgeIdentityIssueContract"
);

const verificationKeyIpfsId = "Qme3iSbzinTvFPbKp7Y6rrVtyKto11xzSa3Pi8dfWU9Wnz";

module.exports = function (deployer) {
  deployer.deploy(ZeroKnowledgeIdentityIssueContract, verificationKeyIpfsId);
};
