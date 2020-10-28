const Contract = artifacts.require("ZeroKnowledgeIdentityIssueContract");

const wallet = "${SIGNING_WALLET}";
const proofIpfsId = "${IPFS_IDR}";

contract("ZeroKnowledgeIdentityIssueContract", async (accounts) => {
  it("should issue an identity token", async () => {
    const contract = await Contract.deployed();
    await contract.issueIdentityToken(wallet, proofIpfsId, { from: wallet });
    const balanceOf = await contract.balanceOf(wallet, { from: wallet });
    assert(balanceOf == 1);
  });
});
