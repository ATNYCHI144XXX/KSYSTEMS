const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("VerifiedAgreement", function () {
  let verifiedAgreement;
  let owner, signer1, signer2, signer3, nonSigner;
  let agreementHash;

  beforeEach(async function () {
    // Get signers
    [owner, signer1, signer2, signer3, nonSigner] = await ethers.getSigners();

    // Create agreement hash
    agreementHash = ethers.keccak256(ethers.toUtf8Bytes("Test Agreement Content"));

    // Deploy contract
    const VerifiedAgreement = await ethers.getContractFactory("VerifiedAgreement");
    verifiedAgreement = await VerifiedAgreement.deploy(
      [signer1.address, signer2.address, signer3.address],
      2, // threshold
      agreementHash
    );
    await verifiedAgreement.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should set the correct signers", async function () {
      expect(await verifiedAgreement.isSigner(signer1.address)).to.be.true;
      expect(await verifiedAgreement.isSigner(signer2.address)).to.be.true;
      expect(await verifiedAgreement.isSigner(signer3.address)).to.be.true;
      expect(await verifiedAgreement.isSigner(nonSigner.address)).to.be.false;
    });

    it("Should set the correct threshold", async function () {
      expect(await verifiedAgreement.threshold()).to.equal(2);
    });

    it("Should set the correct agreement hash", async function () {
      expect(await verifiedAgreement.agreementHash()).to.equal(agreementHash);
    });

    it("Should initialize with zero signatures", async function () {
      expect(await verifiedAgreement.signatureCount()).to.equal(0);
    });

    it("Should not be executed initially", async function () {
      expect(await verifiedAgreement.isExecuted()).to.be.false;
    });

    it("Should emit AgreementCreated event", async function () {
      const VerifiedAgreement = await ethers.getContractFactory("VerifiedAgreement");
      await expect(
        VerifiedAgreement.deploy(
          [signer1.address, signer2.address],
          2,
          agreementHash
        )
      )
        .to.emit(VerifiedAgreement, "AgreementCreated")
        .withArgs(agreementHash, [signer1.address, signer2.address], 2);
    });

    it("Should revert with invalid threshold (zero)", async function () {
      const VerifiedAgreement = await ethers.getContractFactory("VerifiedAgreement");
      await expect(
        VerifiedAgreement.deploy([signer1.address], 0, agreementHash)
      ).to.be.revertedWithCustomError(VerifiedAgreement, "InvalidThreshold");
    });

    it("Should revert with invalid threshold (too high)", async function () {
      const VerifiedAgreement = await ethers.getContractFactory("VerifiedAgreement");
      await expect(
        VerifiedAgreement.deploy([signer1.address], 2, agreementHash)
      ).to.be.revertedWithCustomError(VerifiedAgreement, "InvalidThreshold");
    });

    it("Should revert with empty signers array", async function () {
      const VerifiedAgreement = await ethers.getContractFactory("VerifiedAgreement");
      await expect(
        VerifiedAgreement.deploy([], 1, agreementHash)
      ).to.be.revertedWithCustomError(VerifiedAgreement, "InvalidSigners");
    });
  });

  describe("Signing", function () {
    it("Should allow valid signer to sign", async function () {
      await expect(verifiedAgreement.connect(signer1).sign())
        .to.emit(verifiedAgreement, "Signed")
        .withArgs(signer1.address, 1);

      expect(await verifiedAgreement.hasSigned(signer1.address)).to.be.true;
      expect(await verifiedAgreement.signatureCount()).to.equal(1);
    });

    it("Should allow multiple signers to sign", async function () {
      await verifiedAgreement.connect(signer1).sign();
      await verifiedAgreement.connect(signer2).sign();

      expect(await verifiedAgreement.signatureCount()).to.equal(2);
      expect(await verifiedAgreement.hasSigned(signer1.address)).to.be.true;
      expect(await verifiedAgreement.hasSigned(signer2.address)).to.be.true;
    });

    it("Should revert if non-signer tries to sign", async function () {
      await expect(
        verifiedAgreement.connect(nonSigner).sign()
      ).to.be.revertedWithCustomError(verifiedAgreement, "InvalidSigner");
    });

    it("Should revert if signer tries to sign twice", async function () {
      await verifiedAgreement.connect(signer1).sign();
      await expect(
        verifiedAgreement.connect(signer1).sign()
      ).to.be.revertedWithCustomError(verifiedAgreement, "AlreadySigned");
    });
  });

  describe("Execution", function () {
    it("Should allow execution when threshold is met", async function () {
      await verifiedAgreement.connect(signer1).sign();
      await verifiedAgreement.connect(signer2).sign();

      await expect(verifiedAgreement.connect(owner).execute())
        .to.emit(verifiedAgreement, "AgreementExecuted")
        .withArgs(agreementHash, await ethers.provider.getBlock('latest').then(b => b.timestamp + 1));

      expect(await verifiedAgreement.isExecuted()).to.be.true;
    });

    it("Should revert execution when threshold is not met", async function () {
      await verifiedAgreement.connect(signer1).sign();

      await expect(
        verifiedAgreement.connect(owner).execute()
      ).to.be.revertedWithCustomError(verifiedAgreement, "InsufficientSignatures");
    });

    it("Should revert if trying to execute twice", async function () {
      await verifiedAgreement.connect(signer1).sign();
      await verifiedAgreement.connect(signer2).sign();
      await verifiedAgreement.connect(owner).execute();

      await expect(
        verifiedAgreement.connect(owner).execute()
      ).to.be.revertedWithCustomError(verifiedAgreement, "AlreadyExecuted");
    });

    it("Should revert signing after execution", async function () {
      await verifiedAgreement.connect(signer1).sign();
      await verifiedAgreement.connect(signer2).sign();
      await verifiedAgreement.connect(owner).execute();

      await expect(
        verifiedAgreement.connect(signer3).sign()
      ).to.be.revertedWithCustomError(verifiedAgreement, "AlreadyExecuted");
    });
  });

  describe("View functions", function () {
    it("Should return correct canExecute status", async function () {
      expect(await verifiedAgreement.canExecute()).to.be.false;

      await verifiedAgreement.connect(signer1).sign();
      expect(await verifiedAgreement.canExecute()).to.be.false;

      await verifiedAgreement.connect(signer2).sign();
      expect(await verifiedAgreement.canExecute()).to.be.true;

      await verifiedAgreement.connect(owner).execute();
      expect(await verifiedAgreement.canExecute()).to.be.false;
    });

    it("Should return correct signers list", async function () {
      const signers = await verifiedAgreement.getSigners();
      expect(signers).to.deep.equal([signer1.address, signer2.address, signer3.address]);
    });

    it("Should return correct status", async function () {
      let [current, required, executed] = await verifiedAgreement.getStatus();
      expect(current).to.equal(0);
      expect(required).to.equal(2);
      expect(executed).to.be.false;

      await verifiedAgreement.connect(signer1).sign();
      [current, required, executed] = await verifiedAgreement.getStatus();
      expect(current).to.equal(1);
      expect(required).to.equal(2);
      expect(executed).to.be.false;
    });

    it("Should correctly check if address has signed", async function () {
      expect(await verifiedAgreement.hasAddressSigned(signer1.address)).to.be.false;

      await verifiedAgreement.connect(signer1).sign();
      expect(await verifiedAgreement.hasAddressSigned(signer1.address)).to.be.true;
      expect(await verifiedAgreement.hasAddressSigned(signer2.address)).to.be.false;
    });
  });

  describe("Edge cases", function () {
    it("Should work with threshold equal to number of signers", async function () {
      const VerifiedAgreement = await ethers.getContractFactory("VerifiedAgreement");
      const agreement = await VerifiedAgreement.deploy(
        [signer1.address, signer2.address],
        2, // threshold equals number of signers
        agreementHash
      );
      await agreement.waitForDeployment();

      await agreement.connect(signer1).sign();
      await expect(agreement.connect(owner).execute())
        .to.be.revertedWithCustomError(agreement, "InsufficientSignatures");

      await agreement.connect(signer2).sign();
      await expect(agreement.connect(owner).execute())
        .to.emit(agreement, "AgreementExecuted");
    });

    it("Should work with threshold of 1", async function () {
      const VerifiedAgreement = await ethers.getContractFactory("VerifiedAgreement");
      const agreement = await VerifiedAgreement.deploy(
        [signer1.address],
        1,
        agreementHash
      );
      await agreement.waitForDeployment();

      await agreement.connect(signer1).sign();
      await expect(agreement.connect(owner).execute())
        .to.emit(agreement, "AgreementExecuted");
    });
  });
});
