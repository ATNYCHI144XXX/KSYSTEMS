const { ethers } = require("hardhat");

async function main() {
  console.log("Deploying VerifiedAgreement contract...");

  // Get signers
  const [deployer, signer1, signer2, signer3] = await ethers.getSigners();

  console.log("Deploying with account:", deployer.address);
  console.log("Account balance:", (await ethers.provider.getBalance(deployer.address)).toString());

  // Create agreement hash
  const agreementContent = "This is a test agreement for KSYSTEMS";
  const agreementHash = ethers.keccak256(ethers.toUtf8Bytes(agreementContent));

  console.log("Agreement hash:", agreementHash);

  // Deploy contract
  const VerifiedAgreement = await ethers.getContractFactory("VerifiedAgreement");
  const verifiedAgreement = await VerifiedAgreement.deploy(
    [signer1.address, signer2.address, signer3.address],
    2, // threshold - require 2 out of 3 signatures
    agreementHash
  );

  await verifiedAgreement.waitForDeployment();

  const contractAddress = await verifiedAgreement.getAddress();
  console.log("VerifiedAgreement deployed to:", contractAddress);

  // Verify deployment
  console.log("\nVerifying deployment:");
  console.log("- Signers:", await verifiedAgreement.getSigners());
  console.log("- Threshold:", await verifiedAgreement.threshold());
  console.log("- Agreement hash:", await verifiedAgreement.agreementHash());

  return contractAddress;
}

// Execute deployment
main()
  .then((address) => {
    console.log("\nDeployment successful!");
    process.exit(0);
  })
  .catch((error) => {
    console.error("Deployment failed:", error);
    process.exit(1);
  });
