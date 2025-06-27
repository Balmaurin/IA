import { SheilyApiClient } from '../sheily_utils/sheily_api_client';

describe('SheilyApiClient', () => {
  let apiClient: SheilyApiClient;
  const mockToken = 'test_token';

  beforeEach(() => {
    // Mockear fetch global
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({}),
      })
    ) as jest.Mock;
    
    apiClient = new SheilyApiClient('http://localhost:8000');
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should initialize with base URL', () => {
    expect(apiClient.baseUrl).toBe('http://localhost:8000');
  });

  describe('auth methods', () => {
    it('should call login endpoint', async () => {
      await apiClient.login('testuser', 'password123');
      
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/auth/login', 
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({
            username: 'testuser',
            password: 'password123'
          })
        })
      );
    });

    it('should call register endpoint', async () => {
      await apiClient.register('newuser', 'password123');
      
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/auth/register', 
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({
            username: 'newuser',
            password: 'password123'
          })
        })
      );
    });
  });

  describe('chat methods', () => {
    it('should send chat message', async () => {
      await apiClient.sendChatMessage('Hello', mockToken);
      
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/chat', 
        expect.objectContaining({
          method: 'POST',
          headers: expect.objectContaining({
            'Authorization': `Bearer ${mockToken}`
          }),
          body: JSON.stringify({
            message: 'Hello'
          })
        })
      );
    });

    it('should get chat history', async () => {
      await apiClient.getChatHistory(mockToken);
      
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/chat/history', 
        expect.objectContaining({
          method: 'GET',
          headers: expect.objectContaining({
            'Authorization': `Bearer ${mockToken}`
          })
        })
      );
    });
  });

  describe('token methods', () => {
    it('should get token balance', async () => {
      await apiClient.getTokenBalance(mockToken);
      
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/tokens/balance', 
        expect.objectContaining({
          method: 'GET',
          headers: expect.objectContaining({
            'Authorization': `Bearer ${mockToken}`
          })
        })
      );
    });

    it('should add tokens', async () => {
      await apiClient.addTokens(10, 'task_completion', mockToken);
      
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/tokens/add', 
        expect.objectContaining({
          method: 'POST',
          headers: expect.objectContaining({
            'Authorization': `Bearer ${mockToken}`
          }),
          body: JSON.stringify({
            amount: 10,
            reason: 'task_completion'
          })
        })
      );
    });
  });

  describe('error handling', () => {
    it('should throw on failed requests', async () => {
      (global.fetch as jest.Mock).mockImplementationOnce(() =>
        Promise.resolve({
          ok: false,
          status: 401,
          json: () => Promise.resolve({ error: 'Unauthorized' }),
        })
      );

      await expect(apiClient.login('testuser', 'wrongpass'))
        .rejects
        .toThrow('Request failed with status 401');
    });

    it('should handle network errors', async () => {
      (global.fetch as jest.Mock).mockImplementationOnce(() =>
        Promise.reject(new Error('Network error'))
      );

      await expect(apiClient.login('testuser', 'password123'))
        .rejects
        .toThrow('Network error');
    });
  });
});
