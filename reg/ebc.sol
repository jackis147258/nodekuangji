// SPDX-License-Identifier: MIT
pragma solidity ^0.8.14;
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";



interface IERC20 {
    function decimals() external view returns (uint8);

    function symbol() external view returns (string memory);

    function name() external view returns (string memory);

    function totalSupply() external view returns (uint256);

    function balanceOf(address account) external view returns (uint256);

    function transfer(address recipient, uint256 amount)
    external
    returns (bool);

    function allowance(address owner, address spender)
    external
    view
    returns (uint256);

    function approve(address spender, uint256 amount) external returns (bool);

    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(
        address indexed owner,
        address indexed spender,
        uint256 value
    );
}
//接口
interface stake1 {
function lpPrice() external view returns (uint256);
}
//接口 porxy
interface stake2 {  
function lpPrice() external view returns (uint256);
function getTokenPrice(address pair) external view  returns (uint);
function getTokenPriceLV(address t_pair) external view  returns (uint);
function getETHPx(address pair) external view returns (uint);
function getTokenPriceYmii(address t_pair,address t_pair1) external view  returns (uint);
}

library Math {
    function min(uint256 x, uint256 y) internal pure returns (uint256 z) {
        z = x < y ? x : y;
    }

    // babylonian method (https://en.wikipedia.org/wiki/Methods_of_computing_square_roots#Babylonian_method)
    function sqrt(uint256 y) internal pure returns (uint256 z) {
        if (y > 3) {
            z = y;
            uint256 x = y / 2 + 1;
            while (x < z) {
                z = x;
                x = (y / x + x) / 2;
            }
        } else if (y != 0) {
            z = 1;
        }
    }
}

interface ERC20 {
    function decimals() external view returns (uint8);

    function balanceOf(address account) external view returns (uint256);

    function transfer(address recipient, uint256 amount)
    external
    returns (bool);

    function allowance(address owner, address spender)
    external
    view
    returns (uint256);

    function approve(address spender, uint256 amount) external returns (bool);

    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(
        address indexed owner,
        address indexed spender,
        uint256 value
    );
}

// 安全的数学计算库
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
        if (a == 0) {
            return 0;
        }
        c = a * b;
        assert(c / a == b);
        return c;
    }

    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }

    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }

    function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
        c = a + b;
        assert(c >= a);
        return c;
    }
}

interface IERC721 {
    /**
     * @dev Emitted when `tokenId` token is transferred from `from` to `to`.
     */
    event Transfer(
        address indexed from,
        address indexed to,
        uint256 indexed tokenId
    );

    /**
     * @dev Emitted when `owner` enables `approved` to manage the `tokenId` token.
     */
    event Approval(
        address indexed owner,
        address indexed approved,
        uint256 indexed tokenId
    );

    /**
     * @dev Emitted when `owner` enables or disables (`approved`) `operator` to manage all of its assets.
     */
    event ApprovalForAll(
        address indexed owner,
        address indexed operator,
        bool approved
    );

    /**
     * @dev Returns the number of tokens in ``owner``'s account.
     */
    function balanceOf(address owner) external view returns (uint256 balance);

    /**
     * @dev Returns the owner of the `tokenId` token.
     *
     * Requirements:
     *
     * - `tokenId` must exist.
     */
    function ownerOf(uint256 tokenId) external view returns (address owner);

    /**
     * @dev Safely transfers `tokenId` token from `from` to `to`.
     *
     * Requirements:
     *
     * - `from` cannot be the zero address.
     * - `to` cannot be the zero address.
     * - `tokenId` token must exist and be owned by `from`.
     * - If the caller is not `from`, it must be approved to move this token by either {approve} or {setApprovalForAll}.
     * - If `to` refers to a smart contract, it must implement {IERC721Receiver-onERC721Received}, which is called upon a safe transfer.
     *
     * Emits a {Transfer} event.
     */
    function safeTransferFrom(
        address from,
        address to,
        uint256 tokenId,
        bytes calldata data
    ) external;

    /**
     * @dev Safely transfers `tokenId` token from `from` to `to`, checking first that contract recipients
     * are aware of the ERC721 protocol to prevent tokens from being forever locked.
     *
     * Requirements:
     *
     * - `from` cannot be the zero address.
     * - `to` cannot be the zero address.
     * - `tokenId` token must exist and be owned by `from`.
     * - If the caller is not `from`, it must have been allowed to move this token by either {approve} or {setApprovalForAll}.
     * - If `to` refers to a smart contract, it must implement {IERC721Receiver-onERC721Received}, which is called upon a safe transfer.
     *
     * Emits a {Transfer} event.
     */
    function safeTransferFrom(
        address from,
        address to,
        uint256 tokenId
    ) external;

    /**
     * @dev Transfers `tokenId` token from `from` to `to`.
     *
     * WARNING: Usage of this method is discouraged, use {safeTransferFrom} whenever possible.
     *
     * Requirements:
     *
     * - `from` cannot be the zero address.
     * - `to` cannot be the zero address.
     * - `tokenId` token must be owned by `from`.
     * - If the caller is not `from`, it must be approved to move this token by either {approve} or {setApprovalForAll}.
     *
     * Emits a {Transfer} event.
     */
    function transferFrom(
        address from,
        address to,
        uint256 tokenId
    ) external;

    /**
     * @dev Gives permission to `to` to transfer `tokenId` token to another account.
     * The approval is cleared when the token is transferred.
     *
     * Only a single account can be approved at a time, so approving the zero address clears previous approvals.
     *
     * Requirements:
     *
     * - The caller must own the token or be an approved operator.
     * - `tokenId` must exist.
     *
     * Emits an {Approval} event.
     */
    function approve(address to, uint256 tokenId) external;

    /**
     * @dev Approve or remove `operator` as an operator for the caller.
     * Operators can call {transferFrom} or {safeTransferFrom} for any token owned by the caller.
     *
     * Requirements:
     *
     * - The `operator` cannot be the caller.
     *
     * Emits an {ApprovalForAll} event.
     */
    function setApprovalForAll(address operator, bool _approved) external;

    /**
     * @dev Returns the account approved for `tokenId` token.
     *
     * Requirements:
     *
     * - `tokenId` must exist.
     */
    function getApproved(uint256 tokenId)
    external
    view
    returns (address operator);

    /**
     * @dev Returns if the `operator` is allowed to manage all of the assets of `owner`.
     *
     * See {setApprovalForAll}
     */
    function isApprovedForAll(address owner, address operator)
    external
    view
    returns (bool);

    function safeMint(address to, uint256 tokenId) external;
}
// Import the IUniswapV2Pair interface
interface IUniswapV2Pair {
    function getReserves() external view returns (uint112 reserve0, uint112 reserve1, uint32 blockTimestampLast);
    function token0() external view returns (address);
    function token1() external view returns (address);
}
contract StakeEbcV13 is Initializable,OwnableUpgradeable {
    function initialize(address owner)public initializer{
		__Context_init_unchained();
		__Ownable_init_unchained(owner);//初始化 管理者
        _rewardToken = 0xa643953d39e1f58c1e834A9708160F7357a3ae89; //ymii返还币
        _stakeToken = 0x6b6b2D8166D13b58155b8d454F239AE3691257A6; //质押合约
        _lpPriceToken = 0xB1bF470A9720F8d2E49512DbbcCf7180e4Ac4679; //stake 老合约 获取lprice
        _aToken = 0xc2132D05D31c914a87C6611C10748AEb04B58e8F; //usdt合约
        _bToken = 0x242fD8e9f9271Aca512f75b91535fdd735A27053; //ebc合约
        //收钱钱包    
        _adminToken = 0xFba10176c4CAf393E83459196a72d15B3B723727; //质押合约    
        _outToken = 0x07ed0ef73c009ab5e2D37692c41DCFB052669c8f; //质押合约           
         
        _stake1 = 24 hours * 30 * 1; //质押1月
        _stake3 = 24 hours * 30 * 3; //质押3月
        _stake5 = 24 hours * 30 * 5; //质押5月
        _proportion = 1000; //u兑换币比例    
        _lpPriceTokenNew = 0x1fa2971171FD2e5406b15cc950E5449f9778FC73; //stakenew  获取lprice 
        _lpToken = 0xC008e4834e384Bb494a921500b3889dc5a08A25e; //lp pancake  ymii/usdt    
        _wei=1000000;  //19个0 被除 去掉 18个0  
        isStakeStart = true; //开始 质押
        isClaimStart = true;// 开始 领取
        _priceLp=1;
	}
    address public _rewardToken ; //子币合约
    address public _stakeToken ; //质押合约
    address public _lpPriceToken; //stake 老合约 获取lprice
    address public _aToken ; //usdt合约
    address public _bToken ; //ebc合约
    //收钱钱包    
    address public _adminToken ; //质押合约 
    address public _outToken ; //质押合约                       
    uint256 public _stake1 ; //质押1月
    uint256 public _stake3 ; //质押3月
    uint256 public _stake5 ; //质押5月
    uint256 public _proportion; //u兑换币比例   
    bool public isStakeStart = true; //是否开始质押
    bool public isClaimStart = true; //是否开始领取收益
    string public words; // 字符串，可以通过逻辑合约的函数改变
    mapping(address => address) public _inviterMap; //邀请人
    mapping(address => uint256) public _inviterReward; //邀请人返佣
    mapping(address => uint256) public _inviteNum; //邀请人数
    mapping(address => uint256) public _userStake; //用户质押数量
    mapping(address => uint256) public _userStakeA; //用户质押aToken数量
    mapping(address => uint256) public _userStakeB; //用户质押bToken数量
    mapping(address => uint256) public _userStakeTime; //用户质押时间
    mapping(address => uint256) public _userStakeStartTime; //用户开始质押时间
    mapping(address => uint256) public _userLastClaimTime; //用户最后一次领取时间
    mapping(address => uint256) public _userEndClaimTime; //结束时间
    mapping(address => uint256) public _userPower; //用户个人算力
    mapping(address => bool) public _userBlacklist; //黑名单
    mapping(address => uint256) public _userStakeMonthlyearnings; //月收益
    
    // mapping(address => uint8) public _userReleaseDue; //用户到期释放
    address public _lpPriceTokenNew; //stake  获取lprice
    address public _lpToken; //ymii/usdt lp token
    uint256 public _wei ; //19个0 被除 去掉 18个0 
    mapping(address => uint256) public _userMoonClaimTime; //用户最后一次30天月结时间
    mapping(address => uint256) public _userMoonClaimNumber; //用户moon结 次数 默认 5此

    uint256 public _priceLp ; //质押3月
    
     

     //测试
    function _weiSet(uint256 token) public{
        _wei = token;
    } 

    //测试
    function foo() public{
        words = "news";
    } 
      //设置_lpToken
    function set_priceLp(uint256 token) public onlyOwner {
        _priceLp = token;
    }
     //设置_lpToken
    function set_lpToken(address token) public onlyOwner {
        _lpToken = token;
    }
         //设置_lpToken
    function set_lpPriceTokenNew(address token) public onlyOwner {
        _lpPriceTokenNew = token;
    }
    //设置_aToken
    function set_aToken(address token) public  onlyOwner {
        _aToken = token;
    }
    //设置_bToken
    function set_bToken(address token) public onlyOwner {
        _bToken = token;
    }
     //设置_rewardToken
    function set_rewardToken(address token) public onlyOwner {
        _rewardToken = token;
    }
    //设置_adminToken
    function set_adminToken(address token) public onlyOwner {
        _adminToken = token;
    }
     //设置_adminToken
    function set_outToken(address token) public onlyOwner {
        _outToken = token;
    }

    
    //设置老合约Token _stakeOldToken
    function setlpPriceToken(address token) public onlyOwner {
        _lpPriceToken = token;
    }
    //设置U兑换比例
    function setProportion(uint256 proportion_) public onlyOwner {
        _proportion = proportion_;
    }
    //设置黑名单
    function setUserBlacklist(address user) public onlyOwner {
        _userBlacklist[user] = !_userBlacklist[user];
    }
    //设置质押合约
    function setStakeToken(address token) public onlyOwner {
        _stakeToken = token;
    }
    //设置开关
    function setStatus(bool stakeStart, bool claimStart) public onlyOwner {
        isStakeStart = stakeStart;
        isClaimStart = claimStart;
    }   
    //提现主币
    function withdraw() external onlyOwner {
        payable(msg.sender).transfer(address(this).balance);
    }
   
    function withdrawAllTokens(address token) external onlyOwner {
        uint256 balance = IERC20(token).balanceOf(address(this)); // 获取合约账户的代币余额
        IERC20(token).transfer(msg.sender, balance); // 转移所有代币到调用者账户
    }

            



    //管理员设置用户状态
    function ownerSetUser(
        address user,
        uint256 amount,
        uint256 amountA,
        uint256 amountB,
        uint256 stakeTime,
        uint256 stakeStartTime,
        uint256 userLastClaim,
        uint256 userPower,
        uint256 userEndClaimTime,
        uint256 userStakeMonthlyearnings
    ) public onlyOwner {
        _userStake[user] = amount;
        _userStakeA[user] = amountA;
        _userStakeB[user] = amountB;
        _userStakeTime[user] = stakeTime;
        _userStakeStartTime[user] = stakeStartTime;
        _userLastClaimTime[user] = userLastClaim;
        _userPower[user] = userPower;
        _userEndClaimTime[user] = userEndClaimTime;
        _userStakeMonthlyearnings[user] = userStakeMonthlyearnings;
    } 



    //管理员设置用户状态
    function _userMoonClaimTimeSet(
        address user,
        uint256 userMoonClaimTime     
    ) public onlyOwner {       
        _userMoonClaimTime[user] = userMoonClaimTime;
    }

     //管理员设置用户状态
    function _userStakeABSet(
        address user,
        uint256 amount,
        uint256 amountA,
        uint256 amountB
       
    ) public onlyOwner {
        _userStake[user] = amount;
        _userStakeA[user] = amountA;
        _userStakeB[user] = amountB;
       
    } 

    //管理员设置用户状态
    function _userLastClaimTimeSet(
        address user,      
        uint256 userLastClaim    
    ) public onlyOwner {       
        _userLastClaimTime[user] = userLastClaim;      
    }

    //管理员设置用户状态
    function _userEndClaimTimeSet(
        address user,      
        uint256 userEndClaimTime       
    ) public onlyOwner {       
        _userEndClaimTime[user] = userEndClaimTime;        
    }

    //管理员设置用户状态
    function _userStakeStartTimeSet(
        address user,       
        uint256 stakeStartTime      
    ) public onlyOwner {      
        _userStakeStartTime[user] = stakeStartTime;         
    }

      //管理员设置用户状态stakeTime
    function _userStakeTimeSet(
        address user,       
        uint256 stakeTime
    ) public onlyOwner {       
        _userStakeTime[user] = stakeTime;       
    }

          //管理员设置用户状态_userMoonClaimTime
    function  UserMoonClaimTimeSet(
        address user,       
        uint256 MoonClaimTime
    ) public onlyOwner {       
        _userMoonClaimTime[user] = MoonClaimTime;       
    }
             //管理员设置用户状态_userMoonClaimNumber
    function  _userMoonClaimNumberSet(
        address user,       
        uint256 MoonClaimNumber
    ) public onlyOwner {       
        _userMoonClaimNumber[user] = MoonClaimNumber;       
    }




    // //函数内部
    // function lpPrice() public view returns (uint256) {        
    //     // uint256 price=stake1(_lpPriceToken).lpPrice();
    //     uint256 price=stake2(_lpPriceTokenNew).lpPrice();   //1850
    //     // uint256 price=stake1(0xB1bF470A9720F8d2E49512DbbcCf7180e4Ac4679).lpPrice();
    //     return price;
    // }
     //函数内部 利率 lv
    function TokenPriceLV() public view returns (uint256) {        
        uint256 price=stake2(_lpPriceTokenNew).getTokenPriceLV(_lpToken);   //8241925389884116 ymii     10000000000000000 usdt 获取 u/ymii=12000..
        // uint256 price=1200000000000000000;       
        return price;
    }

    function TokenPriceYmii() public view returns (uint256) {        
        // address t_1=0x02Fa571EdAd13043EE3f3676E65092c5000E3Ad0;
        uint256 price=stake2(_lpPriceTokenNew).getTokenPriceYmii(_lpToken,_lpToken);   //8241925389884116 ymii     10000000000000000 usdt 获取 u/ymii=12000..
        // uint256 price=1200000000000000000;       
        
        return price;
    }



 event ceshi(uint256 indexed beishu, uint256 indexed ymii, uint256 base);
        // //到期取消质押
    function cancalStack() public {                
        require( block.timestamp - _userStakeStartTime[msg.sender] >= _userStakeTime[msg.sender],"not time");        
        require(_userStakeA[msg.sender] > 0, "not StakeA");
        require(_userStakeB[msg.sender] > 0, "not stakeB");
        require(_userMoonClaimTime[msg.sender] >= _userEndClaimTime[msg.sender], "userMoonClaimTime litte");
         require(_userMoonClaimNumber[msg.sender] >= 5, "userMoonClaimNumber litte");
         //最后Moon提取时间大于结束时间  _priceLp

        // uint256 t_rewardTokenNumber=SafeMath.mul(
        //             SafeMath.mul(
        //                     SafeMath.div(SafeMath.div(_userStakeA[msg.sender],70),_wei),
        //                 TokenPriceLV()),
        //                 100);
        uint256 t_rewardTokenNumber=SafeMath.mul(
                    SafeMath.mul(
                            SafeMath.div(SafeMath.div(_userStakeA[msg.sender],70),_wei),
                         getTokenPriceYmii()),
                        100);
        emit ceshi(block.timestamp, t_rewardTokenNumber, 0);

        IERC20(_rewardToken).transfer(msg.sender, t_rewardTokenNumber);
        
        // IERC20(_rewardToken).transferFrom(_outToken,msg.sender,t_rewardTokenNumber);

        // _userStake[msg.sender] = 0;
        _userStakeA[msg.sender] = 0;
        _userStakeB[msg.sender] = 0;
        _userStakeStartTime[msg.sender] = 0;
        _userEndClaimTime[msg.sender] = 0;
        _userStakeTime[msg.sender] = 0;
        // _userPower[msg.sender] = 0;      
        _userMoonClaimTime[msg.sender]=0;
        _userMoonClaimNumber[msg.sender]=0;
            
    }        
        //领取质押收益
    function claimStakeReward() public {
        require(isClaimStart, "ClaimStart flase");
        // require(_userStake[msg.sender] > 0, "not stake");
        require(_userStakeA[msg.sender] > 0, "not StakeA");
        require(_userStakeB[msg.sender] > 0, "not stakeB");
        require(!_userBlacklist[msg.sender], "user is in blacklist");
        // require(
        //     _userLastClaimTime[msg.sender]+ 15 < block.timestamp , //15秒内
        //     "already claimed 15 seconds ago"
        // );
        uint256 amount = pureAmountMoon(msg.sender);
         emit ceshi(block.timestamp, amount, 0);
        //更新领取时间
        _userLastClaimTime[msg.sender] = block.timestamp;
        _userMoonClaimTime[msg.sender] = _userMoonClaimTime[msg.sender]+_stake1;
        _userMoonClaimNumber[msg.sender] = _userMoonClaimNumber[msg.sender]+1;

          // Attempt to transfer the reward tokens
        bool success = IERC20(_rewardToken).transfer(msg.sender, amount);
        require(success, "Token transfer failed. Please try again later.");

    
        // IERC20(_rewardToken).transferFrom(_outToken,msg.sender,  amount);
    }

    // event ceshi1(uint256 indexed beishu, uint256 indexed ymii, uint256 base);
     //计算质押收益
    function pureAmountMoon(address user) public view returns (uint256) {
         
        // require(_userStake[msg.sender] > 0, "not stake");
        require(_userStakeA[msg.sender] > 0, "not StakeA");
        require(_userStakeB[msg.sender] > 0, "not stakeB");
        require(_userMoonClaimTime[msg.sender] <= _userEndClaimTime[msg.sender], "userMoonClaimTime biger");//moon结束时间 小于 结束时间 结束时间 增加 60秒 可能的延时时间
        require(_userMoonClaimNumber[msg.sender] < 5, "userMoonClaimNumber biger");//moon次数 小于5  默认为零

        require(block.timestamp > _userMoonClaimTime[user], "block.times  litter");   //如果当前时间大于30天月结时间
        uint256 t_backUsdt=0;
         //最后Moon提取时间大于结束时间               
              
                    //算上个月 30天的账： 价值 每份10u的 对应 的ymii 数量  _priceLp   getTokenPriceYmii
                    
                    t_backUsdt = SafeMath.mul(
                    SafeMath.mul(
                            SafeMath.div(SafeMath.div(_userStakeA[msg.sender],70),_wei),
                        getTokenPriceYmii()),
                        10);        

                    // t_backUsdt = SafeMath.mul(
                    // SafeMath.mul(
                    //         SafeMath.div(SafeMath.div(_userStakeA[msg.sender],70),_wei),
                    //     _priceLp),
                    //     10);         

                    //     uint256 t_1=SafeMath.div(_userStakeA[msg.sender],70);
                    //     uint256 t_2=SafeMath.div(SafeMath.div(_userStakeA[msg.sender],70),_wei);                                            
                    //  emit ceshi(t_1,t_2,TokenPriceLV());
       
         return t_backUsdt; 
    }

    
     
    //  //计算质押收益
    // function pureAmount(address user) public view returns (uint256) {
    //     uint256 stakeTotalTime;
    //     //间隔周期
    //     stakeTotalTime = block.timestamp - _userLastClaimTime[user];
    //     //没提取过按开始时间算
    //     if (_userLastClaimTime[user] == 0 && _userStake[user] > 0) {
    //         stakeTotalTime = block.timestamp - _userStakeStartTime[user];
    //     }
    //     //没质押返回0
    //     if (_userStake[user] == 0) {
    //         return 0;
    //     }
    //     //如果当前时间大于到期时间
    //     if (block.timestamp > _userEndClaimTime[user]) {
    //         if(_userLastClaimTime[user]==0){
    //             stakeTotalTime = _userEndClaimTime[user] - _userStakeStartTime[user];
    //         }else{
    //             stakeTotalTime = _userEndClaimTime[user] - _userLastClaimTime[user];
    //         }
    //     }
    //     //最后提取时间大于结束时间
    //     if (_userLastClaimTime[user] > _userEndClaimTime[user]) {
    //         return 0;
    //     }
    //     uint256 t_backUsdt=SafeMath.mul(stakeTotalTime, _userPower[user]);
    //      //等于多少ymii  得到 ymii 的价格 
    //       return t_backUsdt;        
    // }

    event ymiiFanhuan(uint256 indexed beishu, uint256 indexed ymii, uint256 base);
    // 质押  通过 amountA usdt 数量 计算 70是一份 等于100
    function stake(
        uint256 amountA,
        uint256 amountB,
        // address inviter,
        uint256 time
    ) public {
        require(isStakeStart, "not start");
        // require(inviter != msg.sender, "inviter cant by self");
        require(_userStake[msg.sender] == 0, "already stake");
        require(_userStakeA[msg.sender] == 0, "already stakeUsdt");
        require(_userStakeB[msg.sender] == 0, "already stakeBdc");        
        require(amountA > 0, "zero amountA");
        require(amountB > 0, "zero amountB");
        require(
            time == _stake1 || time == _stake3 || time == _stake5,
            "not right time"
        );
       
        // if (inviter != address(0)) {
        //     _inviterMap[msg.sender] = inviter;
        //     _inviterReward[inviter] +=
        //     (_lpPrice * amount * 5 * _proportion) /
        //     100000;
        //     _inviteNum[inviter] += 1;
        // }

      
        //收 ymii  和 ebc 两分钱
        IERC20(_aToken).transferFrom(msg.sender, address(this), amountA);        
        IERC20(_bToken).transferFrom(msg.sender, address(this), amountB);

        IERC20(_aToken).transfer(_adminToken, amountA);
        IERC20(_bToken).transfer(_adminToken, amountB);

        // emit ymiiFanhuan(t_Monthlyearnings, SafeMath.mul(TokenPriceLV(), t_Monthlyearnings), base);
            //5个月后返还的 ymii数量  
        uint256 t_blocktime = block.timestamp;
        _userStakeA[msg.sender] = amountA;
        _userStakeB[msg.sender] = amountB;          
        _userStakeStartTime[msg.sender] = t_blocktime;
        _userLastClaimTime[msg.sender]= t_blocktime;
        _userEndClaimTime[msg.sender] = t_blocktime + time;
        _userStakeTime[msg.sender] = time;
        // _userPower[msg.sender] = base;
        _userMoonClaimTime[msg.sender]=t_blocktime+_stake1;//第一次 +30天 月结时间
        _userMoonClaimNumber[msg.sender]=0;//第一次 默认为零
    }

    
    //管理员设置用户状态
    function stakeTestSet(
        address userAddr,
        uint256 userStakeA,
        uint256 userStakeB,
        uint256 userStakeStartTime,
        uint256 userLastClaimTime,
        uint256 userEndClaimTime,
        uint256 userStakeTime,
        uint256 userMoonClaimTime,
        uint256 userMoonClaimNumber
     ) public  {

        require(isSetUser, "Setting user is not allowed currently"); // Check if isSetUser is true
        _userStakeA[userAddr] = userStakeA;
        _userStakeB[userAddr] = userStakeB;
        _userStakeStartTime[userAddr] = userStakeStartTime;
        _userLastClaimTime[userAddr] = userLastClaimTime;
        _userEndClaimTime[userAddr] = userEndClaimTime;
        _userStakeTime[userAddr] = userStakeTime;
        _userMoonClaimTime[userAddr] = userMoonClaimTime;
        _userMoonClaimNumber[userAddr] = userMoonClaimNumber;
    
    } 

      bool public isSetUser; // New state variable to control ownerSetUser

    // Function to allow the owner to set the isSetUser flag
    function setIsSetUser(bool _isSetUser) public onlyOwner {
        isSetUser = _isSetUser;
    }

      address public _pancakeRouter= 0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff;  //pancake Router 地址 
    // Function to get the price of the ymii token using Uniswap V2 pair reserves
    function getTokenPriceYmii() public view returns (uint256) {
        IUniswapV2Pair pair = IUniswapV2Pair(_lpToken);
        (uint112 reserve0, uint112 reserve1, ) = pair.getReserves();
        
        // Since token0 is ymii (18 decimals) and token1 is usdt (6 decimals),
        // adjust the calculation to account for the difference in decimal places
        return (uint256(reserve1) * 1e18) / (uint256(reserve0) * 1e12);
    }

    // Function to get the price of 1 usdt in terms of ymii
    function getUsdtPriceInYmii() public view returns (uint256) {
        IUniswapV2Pair pair = IUniswapV2Pair(_lpToken);
        (uint112 reserve0, uint112 reserve1, ) = pair.getReserves();
        
        // Since token0 is ymii (18 decimals) and token1 is usdt (6 decimals),
        // adjust the calculation to account for the difference in decimal places
        return (uint256(reserve0) * 1e12) / uint256(reserve1);
    }
}

