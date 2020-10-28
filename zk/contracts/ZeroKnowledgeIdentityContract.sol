pragma solidity ^0.4.24;


contract ERC721 {
  function totalSupply() public view returns (uint256 total);
  function balanceOf(address _owner) public view returns (uint256 balance);
  function ownerOf(uint256 _tokenId) external view returns (address owner);
  function approve(address _to, uint256 _tokenId) external;
  function transfer(address _to, uint256 _tokenId) external;
  function transferFrom(address _from, address _to, uint256 _tokenId) external;

  event Transfer(address from, address to, uint256 tokenId);
  event Approval(address owner, address approved, uint256 tokenId);
}

contract ZeroKnowledgeIdentityContract is ERC721 {
  string[] public proofs;

  mapping (uint256 => address) public tokenOwners;
  mapping (address => uint256) public tokenCount;

  function totalSupply() public view returns (uint) {
    return proofs.length;
  }

  function balanceOf(address _owner) public view returns (uint256 count) {
    return tokenCount[_owner];
  }

  function ownerOf(uint256 _tokenId) external view returns (address owner) {
    owner = tokenOwners[_tokenId];
    require(owner != address(0));
  }

  function approve(address _to, uint256 _tokenId) external {
    // No required as tokens can not be transfered
    revert();
  }

  function transfer(address _to, uint256 _tokenId) external {
    // No required as tokens can not be transfered
    revert();
  }

  function transferFrom(address _from, address _to, uint256 _tokenId) external {
    // No required as tokens can not be transfered
    revert();
  }

  function tokensOfOwner(address _owner) external returns (uint256[] tokenIds) {
    uint256 tokenCount = balanceOf(_owner);

    if (tokenCount == 0) {
      return new uint256[](0);
    }

    uint256[] memory result = new uint256[](1);
    uint256 totalCount = totalSupply();

    for (uint8 tokenId = 0; tokenId < totalCount; tokenId++) {
      if (tokenOwners[tokenId] == _owner) {  
        result[0] = tokenId;
      }
    }

    return result;
  }
}

contract Ownable {
  address private _owner;

  modifier onlyOwner() {
    require(isOwner());
    _;
  }

  constructor() public {
    _owner = msg.sender;
  }

  function owner() public view returns (address) {
    return _owner;
  }

  function isOwner() public view returns (bool) {
    return msg.sender == _owner;
  }
}

contract ZeroKnowledgeIdentityIssueContract is ZeroKnowledgeIdentityContract, Ownable {
  string public verificationKey;

  constructor(string _verificationKey) public {
    verificationKey = _verificationKey;
  }

  function issueIdentityToken(
    address _to,
    string _proof
  ) external onlyOwner {
    require(balanceOf(_to) == 0, "Identity has already been issued!");

    uint256 tokenId = proofs.push(_proof) - 1;

    // Issue proof to receiver address
    tokenOwners[tokenId] = _to;
    tokenCount[_to] = 1;

    emit Transfer(address(0), _to, tokenId);
  }
}