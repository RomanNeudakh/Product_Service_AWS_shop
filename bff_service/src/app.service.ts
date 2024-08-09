import { Injectable, HttpException, HttpStatus } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { HttpService } from '@nestjs/axios';
import { AxiosResponse } from 'axios';
import { firstValueFrom } from 'rxjs';
type Config = {
  url: string;
  method: string;
  params?: string;
  data?: Array<Item>;
};
type Item = {
  count: number;
  description: string;
  price: number;
  title: string;
};
@Injectable()
export class AppService {
  constructor(
    private readonly httpService: HttpService,
    private readonly configService: ConfigService,
  ) {}
  async handleRequest(
    recipientServiceName: string,
    query: string,
    method: string,
    body: any,
  ): Promise<AxiosResponse> {
    const recipientURL = this.configService.get<string>(
      `${recipientServiceName.toUpperCase()}_SERVICE_URL`,
    );
    if (!recipientURL) {
      throw new HttpException('Cannot process request', HttpStatus.BAD_GATEWAY);
    }
    try {
      const config: Config = {
        url: recipientURL,
        method: method,
        params: query,
      };
      if (body && Object.keys(body).length > 0) {
        config.data = body;
      }
      const response = await firstValueFrom(this.httpService.request(config));
      return response;
    } catch (error) {
      throw new HttpException(
        error.response?.data || 'some error occurred',
        error.response?.status || HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }
}
