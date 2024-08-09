import { Controller, All, Req, Res, Param, Query, Body } from '@nestjs/common';
import { Request, Response } from 'express';
import { AppService } from './app.service';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @All(':recipientServiceName')
  async handleAll(
    @Param('recipientServiceName') recipientServiceName: string,
    @Req() req: Request,
    @Res() res: Response,
    @Query() query: string,
    @Body() body: any,
  ) {
    try {
      const response = await this.appService.handleRequest(
        recipientServiceName,
        query,
        req.method,
        body,
      );
      res.status(response.status).send(response.data);
    } catch (error) {
      res.status(error.status).send({
        message: error.response?.message || error.response,
        statusCode: error.status,
      });
    }
  }
}
